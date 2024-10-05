from fastapi import APIRouter, HTTPException, WebSocket
from fastapi.websockets import WebSocketDisconnect
from redis import Redis
import json
import asyncio
from pydantic import BaseModel
from redis_client import client
router = APIRouter()

RIDES = ["roller-coaster", "ferris-wheel", "bumper-cars", "carousel", "log-flume"]
class QueueRequest(BaseModel):
    rideId: str
    userId: str

@router.post("/enqueue")
def enqueue(request: QueueRequest):
    try:
        client.rpush(f"queue:{request.rideId}", request.userId)
        publish_queue_update(request.rideId)
        return {"message": "대기열에 추가되었습니다."}
    except Exception as e:
        print(f'대기열 추가 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.post("/dequeue/{rideId}")
def dequeue(rideId: str):
    try:
        userId = client.lpop(f"queue:{rideId}")
        if userId:
            publish_queue_update(rideId)
            return {"userId": userId}
        else:
            raise HTTPException(status_code=404, detail="대기열이 비어있습니다.")
    except Exception as e:
        print(f'대기열 제거 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.get("/position/{rideId}/{userId}")
def get_position(rideId: str, userId: str):
    try:
        queue = client.lrange(f"queue:{rideId}", 0, -1)
        if userId in queue:
            position = queue.index(userId) + 1
            return {"rideId": rideId, "userId": userId, "position": position}
        else:
            raise HTTPException(status_code=404, detail="사용자가 대기열에 없습니다.")
    except Exception as e:
        print(f'위치 조회 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.get("/all-queues")
def get_all_queues():
    try:
        all_queues = {}
        for key in client.keys("queue:*"):
            ride_id = key.split(":")[1]
            queue_length = client.llen(key)
            all_queues[ride_id] = queue_length
        return {"queues": all_queues}
    except Exception as e:
        print(f'모든 대기열 조회 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.websocket("/ws/queue_status")
async def websocket_queue_status(websocket: WebSocket):
    await websocket.accept()
    try:
        pubsub = client.pubsub()
        await pubsub.subscribe('queue_updates')

        initial_status = get_all_queue_status()
        await websocket.send_text(json.dumps(initial_status))

        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message['data'])
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        await pubsub.unsubscribe('queue_updates')
    finally:
        await pubsub.close()

def get_all_queue_status():
    all_queues = {}
    for key in client.keys("queue:*"):
        ride_id = key.split(":")[1]
        queue = client.lrange(key, 0, -1)
        all_queues[ride_id] = len(queue)
    return all_queues

def publish_queue_update(rideId: str):
    queue_length = client.llen(f"queue:{rideId}")
    update = json.dumps({rideId: queue_length})
    client.publish('queue_updates', update)