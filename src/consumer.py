import os
from faststream import FastStream
import asyncio
from faststream.rabbit import RabbitBroker
from src.database.mongo_client import get_collection
from src.database.redis_client import incrementar_saldo


broker = RabbitBroker(os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/"))
app = FastStream(broker)


@broker.subscriber(os.getenv("RABBIT_QUEUE", "corridas.finalizadas"))
async def process_corrida(msg: dict):
    coll = get_collection()
    motorista = msg.get("motorista", {}).get("nome", "")
    valor = float(msg.get("valor_corrida", 0.0))
    await incrementar_saldo(motorista, valor)
    await coll.update_one({"id_corrida": msg.get("id_corrida")}, {"$set": msg}, upsert=True)


if __name__ == "__main__":
    asyncio.run(app.run())
