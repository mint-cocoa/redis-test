from fastapi import FastAPI
from routes import queue

app = FastAPI()
app.include_router(queue.router, prefix="/queue")

@app.get("/")
def read_root():
    return {"message": "놀이기구 줄서기 서비스에 오신 것을 환영합니다!"}
