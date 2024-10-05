import os
import redis
import asyncio

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')

pool = redis.ConnectionPool.from_url(redis_url, decode_responses=True)
client = redis.Redis(connection_pool=pool)

# 비동기 Redis 클라이언트를 원하시면 aioredis를 사용할 수 있습니다.
