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