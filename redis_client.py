import os
import redis
import asyncio


RIDES = ["roller-coaster", "ferris-wheel", "bumper-cars", "carousel", "log-flume"]

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
pool = redis.ConnectionPool.from_url(redis_url, decode_responses=True)
client = redis.Redis(connection_pool=pool)
def initialize_rides():
    for ride in RIDES:
        if not client.exists(f"queue:{ride}"):
            client.rpush(f"queue:{ride}", "")  # 빈 문자열로 초기화

initialize_rides()
# 비동기 Redis 클라이언트를 원하시면 aioredis를 사용할 수 있습니다.
