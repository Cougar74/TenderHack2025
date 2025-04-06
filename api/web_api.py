import json
import requests
import time
from copy import deepcopy
from uuid import UUID
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QUERY = []
QUERY2 = []
ANSWER = []
ANSWER2 = []

DB_URL = 'https://design-by-oz.ru/api_go'

async def send_request(url: str, method: str, data: dict = None):
    try:
        if method.upper() == "GET":
            response = requests.get(f'{DB_URL}{url}', params=data)
        elif method.upper() == "POST":
            response = requests.post(f'{DB_URL}{url}', json=data)
        elif method.upper() == "PUT":
            response = requests.put(f'{DB_URL}{url}', json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(f'{DB_URL}{url}', json=data)
        else:
            return {"error": "Unsupported HTTP method"}
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/")
async def read_root():
    return {"message": "Welcome to TenderHack2025 API"}

@app.get("/api/history/{uuid}")
async def get_user_history(uuid: UUID):
    print(f'User history: {uuid}')
    
    response = await send_request(f'/historyUser/{uuid}', method='GET')
    
    data = response['response']
    for d in data:
        if d.get('Responce') is not None:
            d['Responce'] = json.loads(d['Responce'])
    
    return {
        'history': data
    }

@app.get("/api/models/query")
async def awaiting_query():
    global QUERY
    
    if len(QUERY):
        data = QUERY.pop()
        
        return {
            'query': data
        }
        
# @app.get("/api/models/query2")
# async def awaiting_query2():
#     global QUERY2
    
#     if len(QUERY2):
#         data = QUERY2.pop()
        
#         return {
#             'query': data
#         }
    
@app.post("/api/models/query")
async def awaiting_query(data: dict):
    global ANSWER
    
    ANSWER.append(deepcopy(data))
    
# @app.post("/api/models/query2")
# async def awaiting_query(data: dict):
#     global ANSWER2
    
#     ANSWER2.append(deepcopy(data))
    
@app.post("/api/query/{uuid}")
async def post_user_query(uuid: UUID, body: dict):
    global QUERY, ANSWER, QUERY2, ANSWER2
    
    query = body.get("query")
    print(f'Get query: {uuid} -- {query}')
    QUERY.append(query)
    # QUERY2.append(query)
    
    data = {'UserUuid': str(uuid), 'Query': query}
    response = await send_request('/history', method='POST', data=data)
    response = response['response']
    
    # await asyncio.sleep(2)
    # while not (len(ANSWER) & len(ANSWER2)):
    #     print(f'Waiting! {len([*ANSWER, *ANSWER2]) = } ---- {len([*QUERY, *QUERY2]) = }')
    #     await asyncio.sleep(0.5)
    
    while not len(ANSWER):
        print(f'Waiting! {len(ANSWER) = } ---- {len(QUERY) = }')
        await asyncio.sleep(0.5)
    
    # data = {**ANSWER.pop(), **ANSWER2.pop()}
    data = ANSWER.pop()
    
    send_data = {'ID': response, 'Responce': json.dumps(data['answer'], ensure_ascii=False), 'ClassificationName': data['class']}
    print(f'{send_data = }')
    await send_request('/history/ResponceAndClassificationName', method='PUT', data=send_data)
    
    links = list({'text': f"{t['source']}, стр.{t['page']}", 'links': f"#{t['page']}"} for t in data['answer']['short_sources'])
    
    return {
        'id': response,
        'answer': data['answer']['short_answer'],
        # 'answer': data['answer']['answer'],
        'links': links
    }
    
    # return {
    #     'id': int(time.time()),
    #     'answer': f'Ну типа что-то выдал на: {query}',
    #     'links': [
    #         {'text': '1234', 'link': '#1'},
    #         {'text': '5678', 'link': '#2'},
    #     ]
    # }

@app.post("/api/set_rate/{id}")
async def post_set_rate(id: int, body: dict):
    rate = body.get("rate")
    
    await send_request('/history/Rating', method='PUT', data={'ID': id, 'Rating': rate})
    
    print(f'Set rate: id={id}, rate={rate}')
    
    return {
        'status': 'success',
        'id': id,
        'rate': rate
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12349)