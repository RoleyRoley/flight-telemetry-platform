# Script to seed fresh database with test data
from datetime import datetime

from app.database import SessionLocal
from app.models import Aircraft, Flight


def seed_database():
    db = SessionLocal()
    
    
    try:
        
        # Check if the aircraft already exists to avoid duplicate entries
        exisiting_aircraft = (
            db.query(Aircraft)
            .filter(Aircraft.aircraft_code == "AIR-001")
            .first()
        )
        
        if exisiting_aircraft:
            print("Aircraft already exists. Skipping seeding.")
            return
        
        aircraft = Aircraft(
            aircraft_code="AIR-001",
            model="Airbus A320"
            
        )
        
        db.add(aircraft)
        db.commit()
        db.refresh(aircraft)
        
        # Create a flight associated with the aircraft
        flight = Flight(
            flight_number="FL-001",
            aircraft_id=aircraft.id,
            departure_airport="EGLL",
            arrival_airport="EHAM",
            scheduled_departure_time=datetime(2026, 6, 18, 12, 0, 0),
            scheduled_arrival_time=datetime(2026, 6, 18, 13, 15, 0),
            status="scheduled"
        )
        
        db.add(flight)
        db.commit()
        
        print("Database seeded successfully.")
        
    finally:
        db.close()
        
if __name__ == "__main__":
    seed_database()