# Table models:

from sqlalchemy import Column, Integer, String
from app.database import Base


# Aircraft model
class Aircraft(Base):
    __tablename__ = "aircraft"
    
    
    id = Column(Integer, primary_key=True, index=True)

    # Aircraft code (e.g., "A320", "B737") - unique identifier for the aircraft
    aircraft_code = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False
    )

    # Aircraft model (e.g., "Airbus A320", "Boeing 737") - descriptive name of the aircraft
    model = Column(
        String,
        nullable=False
    )