from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from starlette.responses import JSONResponse

from application.clients.brokers.kafka.producer import KafkaProducer
from application.dependency.dependency import get_kafka_producer

app = FastAPI(title="Broker API")

kafka_router = APIRouter(
    prefix="/kafka",
    tags=["Kafka"],
)


@kafka_router.post(
    path="/send-message",
)
async def kafka_send_message(
    topic: str,
    message: dict,
    kafka_producer: Annotated[KafkaProducer, Depends(get_kafka_producer)],
) -> JSONResponse:
    await kafka_producer.send(topic, message)
    return JSONResponse(status_code=201, content={"message": "Message has been sent"})


rabbit_router = APIRouter(
    prefix="/rabbit-mq",
    tags=["RabbitMQ"],
)


@rabbit_router.post(
    path="/send-message",
)
async def rmq_send_message() -> dict:
    return {"message": "Hello World"}


app.include_router(kafka_router)
app.include_router(rabbit_router)
