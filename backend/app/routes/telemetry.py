from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TelemetryRecord
from app.schemas import TelemetryCreate

router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"],
)


@router.get("/")
def get_telemetry():
    return {
        "message": "Telemetry endpoint working"
    }

# Create a new telemetry record
@router.post("/")
def create_telemetry(
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db)
):
    # Telemetry record
    new_record = TelemetryRecord(
        flight_id=telemetry.flight_id,
        timestamp=telemetry.timestamp,
        altitude_ft=telemetry.altitude_ft,
        ground_speed_kts=telemetry.ground_speed_kts,
        fuel_percentage=telemetry.fuel_percentage,
        engine_temp_c=telemetry.engine_temp_c,
        flight_phase=telemetry.flight_phase
    )

    # Add the new telemetry record to the database
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # Return the created telemetry record's ID
    return {
        "message": "Telemetry record created successfully.",
        "record_id": new_record.id    }