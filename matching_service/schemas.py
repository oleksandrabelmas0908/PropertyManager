from pydantic import BaseModel


class InputModel(BaseModel):
    user_id: int


class PropertySchema(BaseModel):
    id: int
    title: str
    description: str | None
    city: str  # City name instead of city_id
    bedrooms: int
    price: float
    pets: bool
    pool: bool
    yard: bool
    parking: bool

    class Config:
        from_attributes = True