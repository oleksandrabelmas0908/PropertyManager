from langchain_ollama import ChatOllama
from schema import DataModel

import os


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


def parse_text(text: str) -> DataModel:
    model = ChatOllama(
        model="phi3",
        base_url=OLLAMA_HOST,
        temperature=0
    )

    messages = [
        ("system", "You are proffessional parser. Parse data "),
        ("human", text),
    ]
    
    response = model.with_structured_output(DataModel).invoke(messages)

    return DataModel(
        email=response.email,
        phone=response.phone,
        first_name=response.first_name,
        last_name=response.last_name,
        bedrooms=response.bedrooms,
        max_budget=response.max_budget,
        monthly_income=response.monthly_income,
        day_of_moving_in=response.day_of_moving_in,
        pets=response.pets,
        pool=response.pool,
        yard=response.yard,
        parking=response.parking,
        city=response.city,
    )





