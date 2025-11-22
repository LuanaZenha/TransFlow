import os
from motor.motor_asyncio import AsyncIOMotorClient


_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        _client = AsyncIOMotorClient(url)
    return _client


def get_collection():
    client = get_client()
    db_name = os.getenv("MONGO_DB", "transflow")
    coll_name = os.getenv("MONGO_COLLECTION", "corridas")
    return client[db_name][coll_name]
