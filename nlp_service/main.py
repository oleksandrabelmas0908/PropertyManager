from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import logging
import json
import os
from time import sleep
from contextlib import asynccontextmanager

from schema import DataModel, InputModel
from parcer import parse_text
from broker import get_messages, produce 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting NLP service...")
    # kafka_message_processor()
    yield
    logger.info("Shutting down NLP service...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://api:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/parse/")
async def trigger():
    messages = get_messages(topic="send_to_parse_topic", group_id="nlp_service_group")
    if not messages:
        logger.info("No messages to process.")
        return {"status": "no messages to process"}
    
    for message in messages:
        parsed_data = parse_text(message)
        produce(message=parsed_data.model_dump(), topic="parsed_data_topic")
        logger.info(f"Produced parsed data to 'parsed_data_topic': {parsed_data}")

    return {"status": "data processed"}
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)