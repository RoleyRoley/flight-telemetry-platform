from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating telemetry data
class TelemetryCreate(BaseModel):
    flight_id: int

    timestamp: datetime

    altitude_ft: float
    ground_speed_kts: float

    fuel_percentage: float
    engine_temp_c: float

    flight_phase: str  
    
    
    latitude: float
    longitude: float
    heading_deg: float
    
    route_progress_percentage: float  # Route progress as a percentage (0.0 to 100.0)
    
    

# Schema for Alert response data
class AlertResponse(BaseModel):
    id: int
    flight_id: int
    telemetry_record_id: int
    timestamp: datetime
    severity: str
    message: str

    class Config:
        from_attributes = True

# Schema for Flight Summary response data
class FlightSummaryResponse(BaseModel):
    flight_id: int
    flight_number: str

    departure_airport: str
    arrival_airport: str
    status: str

    duration_seconds: Optional[float]
    telemetry_records: int

    max_altitude_ft: Optional[float]
    max_ground_speed_kts: Optional[float]
    fuel_used_percentage: Optional[float]
    highest_engine_temp_c: Optional[float]

    alerts_generated: int
    outcome: str
    

    