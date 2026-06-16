# Table models:

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.database import Base


# Aircraft model
class Aircraft(Base):
    # Table name
    __tablename__ = "aircraft"
    
    # Columns
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

    # Relationship to the Flight model - allows access to the associated flights for this aircraft
    flights = relationship("Flight", back_populates="aircraft")

class Flight(Base):
    # Table name
    __tablename__ = "flights"

    # Columns
    id = Column(Integer, primary_key=True, index=True)

    # Flight number (e.g., "AA123", "BA456") - unique identifier for the flight
    flight_number = Column(
        String,
        unique=True,
        nullable=False
    )

    # Foreign key to the Aircraft table - links the flight to a specific aircraft
    aircraft_id = Column(
        Integer,
        ForeignKey("aircraft.id"),
        nullable=False
    )

    # Departure airport code (e.g., "JFK", "LHR") - IATA code of the departure airport
    departure_airport = Column(String, nullable=False)
    # Arrival airport code (e.g., "JFK", "LHR") - IATA code of the arrival airport
    arrival_airport = Column(String, nullable=False)

    # Scheduled departure time (e.g., "2024-06-01T10:00:00Z") - ISO 8601 format
    scheduled_departure_time = Column(String, nullable=False)
    # Scheduled arrival time (e.g., "2024-06-01T14:00:00Z") - ISO 8601 format
    scheduled_arrival_time = Column(String, nullable=True)

    # Flight status (e.g., "scheduled", "in-flight", "landed")
    status = Column(String, default="scheduled") 

    # Relationship to the Aircraft model - allows access to the associated aircraft object
    aircraft = relationship("Aircraft", back_populates="flights") 

    # Relationship to the TelemetryRecord model - allows access to the associated telemetry records for this flight
    telemetry_records = relationship(
        "TelemetryRecord",
        back_populates="flight",    
    )


class TelemetryRecord(Base):
    # Table name
    __tablename__ = "telemetry_records"

    # Columns
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the Flight table - links the telemetry record to a specific flight
    flight_id = Column(
        Integer,
        ForeignKey("flights.id"),
        nullable=False
    )

    timestamp = Column(DateTime, nullable=False)  # Timestamp of the telemetry record (ISO 8601 format)
    altitude_ft = Column(Float, nullable=False)  # Altitude in feet
    ground_speed_kts = Column(Float, nullable=False)  # Ground speed in knots
    fuel_percentage = Column(Float, nullable=False)  # Fuel percentage remaining
    engine_temp_c = Column(Float, nullable=False)  # Engine temperature in Celsius
    flight_phase = Column(String, nullable=False)  # Flight phase (e.g., "takeoff", "cruise", "landing")

    # Relationships
    

    flight = relationship(
        "Flight",
        back_populates="telemetry_records",
    )