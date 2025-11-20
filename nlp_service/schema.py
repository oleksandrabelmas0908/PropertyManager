from datetime import date
from pydantic import BaseModel


class DataModel(BaseModel): 
    email: str
    phone: str
    first_name: str
    last_name: str | None = None
    bedrooms: int
    max_budget: float
    monthly_income: float
    day_of_moving_in: date  
    pets: bool 
    pool: bool 
    yard: bool 
    parking: bool 
    city: str