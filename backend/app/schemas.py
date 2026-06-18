from pydantic import BaseModel
from datetime import datetime

# Schema for creating telemetry data
class TelemetryCreate(BaseModel):
    flight_id: int

    timestamp: datetime

    altitude_ft: float
    ground_speed_kts: float

    fuel_percentage: float
    engine_temp_c: float

    flight_phase: str  

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