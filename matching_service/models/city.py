from sqlalchemy import ForeignKey, Integer, String, Column

from db import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, max_length=100)