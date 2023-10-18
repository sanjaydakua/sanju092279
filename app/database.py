# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.models import DBAddress
from geopy.distance import great_circle

DATABASE_URL = "sqlite:///./addressbook.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 #save data after post request       
def create_address(db: Session, address_data):
    db_address = DBAddress(**address_data.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

#read data from db
def read_address(db: Session, address_id: int):
    return db.query(DBAddress).filter(DBAddress.id == address_id).first()

#update data from db
def update_address(db: Session, address_id: int, updated_address_data):
    # Retrieve the address by its ID
    db_address = db.query(DBAddress).filter(DBAddress.id == address_id).first()

    # Check if the address exists
    if db_address:
        # Update the address data with the new values
        for key, value in updated_address_data.dict().items():
            setattr(db_address, key, value)

        # Commit the changes to the database
        db.commit()

    return db_address

#delete data from db
def delete_address(db: Session, address_id: int):
    # Retrieve the address by its ID
    db_address = db.query(DBAddress).filter(DBAddress.id == address_id).first()

    if db_address:
        # Delete the address from the database
        db.delete(db_address)
        db.commit()

    return db_address

def get_addresses_nearby(db: Session, latitude: float, longitude: float, distance: float):
    # Reference point coordinates
    reference_point = (latitude, longitude)

    # Query addresses and calculate distances using Haversine
    addresses = db.query(DBAddress).all()
    addresses_nearby = []

    for address in addresses:
        address_coordinates = (address.latitude, address.longitude)
        distance_km = great_circle(reference_point, address_coordinates).kilometers

        if distance_km <= distance:
            addresses_nearby.append(address)

    return addresses_nearby
