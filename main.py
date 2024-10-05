from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from routes import queue
from redis import Redis

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis 클라이언트 초기화
redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)

# WebSocket 연결을 관리하는 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# 실시간 업데이트를 위한 WebSocket 엔드포인트
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)

# 실시간 업데이트를 수행하는 백그라운드 태스크
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_queue_status())

async def update_queue_status():
    while True:
        status = {}
        for ride in queue.RIDES:
            queue_list = redis_client.lrange(f"queue:{ride}", 0, -1)
            queue_list = [user for user in queue_list if user]  # 빈 문자열 제거
            status[ride] = len(queue_list)
        await manager.broadcast(json.dumps(status))
        await asyncio.sleep(1)  # 1초마다 업데이트

app.include_router(queue.router)
