from datetime import date
from pydantic import BaseModel


class InputModel(BaseModel):
    input_data: str


class DataModel(BaseModel): 
    email: str
    phone: str
    first_name: str
    last_name: str
    bedrooms: int
    max_budget: float
    monthly_income: float
    pets: bool 
    pool: bool 
    yard: bool 
    parking: bool 
    city: str


class DataModelLLM(DataModel): 
    day_of_moving_in: date  


class DataModelParsed(DataModel): 
    day_of_moving_in: str
