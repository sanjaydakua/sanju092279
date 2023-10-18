# app/models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from app.base import Base

class DBAddress(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

class AddressBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
