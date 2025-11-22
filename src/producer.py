import os
from faststream.rabbit import RabbitBroker


broker = RabbitBroker(os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/"))


async def publish_corrida_finalizada(payload: dict):
    await broker.publish(payload, queue=os.getenv("RABBIT_QUEUE", "corridas.finalizadas"))
