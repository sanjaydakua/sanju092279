from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import database, models
from geopy.distance import great_circle

router = APIRouter()
# Import any necessary modules for your database operations

@router.post("/addresses/", response_model=models.Address)
def create_address(address: models.AddressCreate, db: Session = Depends(database.get_db)):
    # Example: Create a new address in the database
    db_address = database.create_address(db, address)
    return db_address

@router.put("/addresses/{address_id}", response_model=models.Address)
def update_address(address_id: int, address: models.AddressUpdate, db: Session = Depends(database.get_db)):
    # Example: Update an address in the database
    db_address = database.update_address(db, address_id, address)
    return db_address

@router.delete("/addresses/{address_id}", response_model=models.Address)
def delete_address(address_id: int, db: Session = Depends(database.get_db)):
    # Example: Delete an address from the database
    db_address = database.delete_address(db, address_id)
    return db_address

@router.get("/addresses/{address_id}", response_model=models.Address)
def read_address(address_id: int, db: Session = Depends(database.get_db)):
    # Example: Retrieve an address from the database
    db_address = database.read_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@router.get("/addresses-nearby/")
def get_addresses_nearby(
    latitude: float = Query(..., description="Latitude of the reference point"),
    longitude: float = Query(..., description="Longitude of the reference point"),
    distance: float = Query(..., description="Maximum distance in kilometers"),
    db: Session = Depends(database.get_db)
):
 # Validate input parameters
    if distance <= 0:
        raise HTTPException(status_code=400, detail="Distance must be greater than 0.")
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude values.")

    # Reference point coordinates
    reference_point = (latitude, longitude)

    # Query addresses and calculate distances using Haversine
    addresses = db.query(models.DBAddress).all()
    addresses_nearby = []   
    
    for address in addresses:
        address_coordinates = (address.latitude, address.longitude)
        distance_km = great_circle(reference_point, address_coordinates).kilometers

        if distance_km <= distance:
            addresses_nearby.append(address)

    return addresses_nearby
    
    
    
    
