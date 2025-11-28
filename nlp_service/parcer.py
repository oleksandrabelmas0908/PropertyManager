from langchain_ollama import ChatOllama
from schema import DataModelLLM, DataModelParsed
from datetime import date

import os
import logging


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_text(text: str) -> DataModelParsed:
    model = ChatOllama(
        model="phi3",
        base_url=OLLAMA_HOST,
        temperature=0
    )

    messages = [
        ("system", "You are proffessional parser. Parse data "),
        ("human", text),
    ]
    
    response = model.with_structured_output(DataModelLLM).invoke(messages)

    logger.info(f"day of moving_in before parsing: {response.day_of_moving_in}")

    return DataModelParsed(
        email=response.email,
        phone=response.phone,
        first_name=response.first_name,
        last_name=response.last_name,
        bedrooms=response.bedrooms,
        max_budget=response.max_budget,
        monthly_income=response.monthly_income,
        day_of_moving_in=str(response.day_of_moving_in),
        pets=response.pets,
        pool=response.pool,
        yard=response.yard,
        parking=response.parking,
        city=response.city,
    )





