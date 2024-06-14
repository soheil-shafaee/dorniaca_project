import aioredis

redis = aioredis.from_url("redis://localhost")

ALLOWED_IPS_KEY= "allowed_ip"

async def is_ip_allowed(ip:str):
    return await redis.sismember(ALLOWED_IPS_KEY, ip)

async def add_ip(ip:str):
    await redis.sadd(ALLOWED_IPS_KEY, ip)

