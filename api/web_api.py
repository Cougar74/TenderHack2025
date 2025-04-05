import json
import requests
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

@app.get("/api/")
async def read_root():
    return {"message": "Welcome to TenderHack2025 API"}

@app.get("/api/history/{uuid}")
async def get_user_history(uuid: UUID):
    print(f'User history: {uuid}')
    
    return {
        'history': [],
    }
    
@app.post("/api/query/{uuid}")
async def post_user_query(uuid: UUID, body: dict):
    query = body.get("query")
    print(f'Get query: {uuid} -- {query}')
    
    await asyncio.sleep(2)
    
    return {
        'id': 1,
        'answer': f'Ну типа что-то выдал на: {query}',
        'links': [
            {'text': '1234', 'link': '#1'},
            {'text': '5678', 'link': '#2'},
        ]
    }

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