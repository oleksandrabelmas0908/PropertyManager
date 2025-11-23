from datetime import datetime
from db import Base
from . import City, Property

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date, Boolean, Table
from sqlalchemy.orm import relationship


# Define the association table that Django created for the many-to-many relationship
users_matches = Table(
    'users_matches',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('property_id', Integer, ForeignKey('properties.id'), nullable=False),
    extend_existing=True
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, max_length=30, nullable=False)
    last_name = Column(String, max_length=30, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    bedrooms = Column(Integer, nullable=True)
    max_budget = Column(Float, nullable=True)
    monthly_income = Column(Float, nullable=True)
    day_of_moving_in = Column(Date, nullable=True)
    pets = Column(Boolean, nullable=True)
    pool = Column(Boolean, nullable=True)
    yard = Column(Boolean, nullable=True)
    parking = Column(Boolean, nullable=True)
    date_created = Column(Date, default=datetime.now(), nullable=False)

    city_id = Column(ForeignKey(City.id), nullable=False)

    # Relationship to matched properties via the Django-created users_matches table
    matches = relationship(
        Property,
        secondary=users_matches
    )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"