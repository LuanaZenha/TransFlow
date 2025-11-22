import os
from redis.asyncio import Redis


_redis: Redis | None = None


def get_redis() -> Redis:
    global _redis
    if _redis is None:
        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _redis = Redis.from_url(url, decode_responses=True)
    return _redis


async def get_saldo(motorista: str) -> float:
    r = get_redis()
    key = f"saldo:{motorista.lower()}"
    v = await r.get(key)
    return float(v) if v is not None else 0.0


async def incrementar_saldo(motorista: str, valor: float) -> float:
    r = get_redis()
    key = f"saldo:{motorista.lower()}"
    await r.incrbyfloat(key, float(valor))
    v = await r.get(key)
    return float(v) if v is not None else 0.0
