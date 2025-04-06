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

@app.get("/api/")
async def read_root():
    return {"message": "Welcome to TenderHack2025 API"}

@app.get("/api/history/{uuid}")
async def get_user_history(uuid: UUID):
    print(f'User history: {uuid}')
    
    return {
        'history': [],
    }

@app.get("/api/models/query")
async def awaiting_query():
    global QUERY
    
    if len(QUERY):
        data = QUERY.pop()
        
        return {
            'query': data
        }
        
@app.get("/api/models/query2")
async def awaiting_query2():
    global QUERY2
    
    if len(QUERY2):
        data = QUERY2.pop()
        
        return {
            'query': data
        }
    
@app.post("/api/models/query")
async def awaiting_query(data: dict):
    global ANSWER
    
    ANSWER.append(deepcopy(data))
    
@app.post("/api/models/query2")
async def awaiting_query(data: dict):
    global ANSWER2
    
    ANSWER2.append(deepcopy(data))
    
@app.post("/api/query/{uuid}")
async def post_user_query(uuid: UUID, body: dict):
    global QUERY, ANSWER, QUERY2, ANSWER2
    
    query = body.get("query")
    print(f'Get query: {uuid} -- {query}')
    QUERY.append(query)
    QUERY2.append(query)
    
    # await asyncio.sleep(2)
    while not (len(ANSWER) & len(ANSWER)):
        print(f'Waiting! {len([*ANSWER, *ANSWER]) = } ---- {len([*QUERY, *QUERY2]) = }')
        await asyncio.sleep(0.5)
    
    data = {**ANSWER.pop(), **ANSWER2.pop()}
    
    links = list({'text': f"{t['source']}, стр.{t['page']}", links: f"#{t['page']}"} for t in data['answer']['short_sources'])
    
    return {
        'id': int(time.time()),
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
    print(f'Set rate: id={id}, rate={rate}')
    
    return {
        'status': 'success',
        'id': id,
        'rate': rate
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12349)