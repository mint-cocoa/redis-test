from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import redis_client

router = APIRouter()

class EnqueueRequest(BaseModel):
    rideId: str
    userId: str

class DequeueRequest(BaseModel):
    rideId: str

@router.post("/enqueue")
def enqueue(request: EnqueueRequest):
    if not request.rideId or not request.userId:
        raise HTTPException(status_code=400, detail="rideId와 userId가 필요합니다.")
    
    try:
        redis_client.client.rpush(f"queue:{request.rideId}", request.userId)
        queue = redis_client.client.lrange(f"queue:{request.rideId}", 0, -1)
        position = queue.index(request.userId) + 1
        return {"message": "줄에 추가되었습니다.", "position": position}
    except Exception as e:
        print(f'enqueue 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.post("/dequeue")
def dequeue(request: DequeueRequest):
    if not request.rideId:
        raise HTTPException(status_code=400, detail="rideId가 필요합니다.")
    
    try:
        user_id = redis_client.client.lpop(f"queue:{request.rideId}")
        if user_id:
            return {"message": "줄에서 제거되었습니다.", "userId": user_id}
        else:
            return {"message": "줄에 사람이 없습니다."}
    except Exception as e:
        print(f'dequeue 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")

@router.get("/status/{rideId}")
def status(rideId: str):
    try:
        queue = redis_client.client.lrange(f"queue:{rideId}", 0, -1)
        return {"rideId": rideId, "queue": queue}
    except Exception as e:
        print(f'status 조회 에러: {e}')
        raise HTTPException(status_code=500, detail="서버 에러")
