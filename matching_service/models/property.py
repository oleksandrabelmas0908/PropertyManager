from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from . import City


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    pets = Column(Boolean, default=False)
    pool = Column(Boolean, default=False)
    yard = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)

    city_id = Column(ForeignKey(City.id), nullable=False)
    
    # Relationship to City
    city = relationship("City")


    def __repr__(self):
        return f"<Property(id={self.id}, city_id={self.city_id}, price={self.price})>"