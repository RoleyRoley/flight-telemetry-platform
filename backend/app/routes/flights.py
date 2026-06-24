from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight, TelemetryRecord, Alert
from app.schemas import FlightSummaryResponse

router = APIRouter(
    prefix="/flights",
    tags=["flights"],
)

# Get flight summary by flight ID
@router.get("/{flight_id}/summary", response_model=FlightSummaryResponse)
def get_flight_summary(
    flight_id: int, 
    db: Session = Depends(get_db)
):
    # Query the database for the flight with the specified flight ID
    flight = (
        db.query(Flight)
        .filter(Flight.id == flight_id)
        .first()
    )

    # Check if the flight exists; if not, raise a 404 error
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")

    
    telemetry_records = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.flight_id == flight_id)
        .order_by(TelemetryRecord.timestamp.asc())
        .all()
    )

    # Count the number of alerts generated for this flight
    alerts_count = (
        db.query(Alert)
        .filter(Alert.flight_id == flight_id)
        .count()
    )

    # If there are no telemetry records, return a summary with default values and an appropriate outcome message
    if not telemetry_records:
        return FlightSummaryResponse(
            flight_id=flight.id,
            flight_number=flight.flight_number,
            departure_airport=flight.departure_airport,
            arrival_airport=flight.arrival_airport,
            status=flight.status,
            duration_seconds=None,
            telemetry_records=0,
            max_altitude_ft=None,
            max_ground_speed_kts=None,
            fuel_used_percentage=None,
            highest_engine_temp_c=None,
            alerts_generated=alerts_count,
            outcome="No telemetry data available"
        )
    
    # Calculate flight summary metrics based on the telemetry records
    
    first_record = telemetry_records[0]
    last_record = telemetry_records[-1]

    duration_seconds = (last_record.timestamp - first_record.timestamp).total_seconds()

    
    max_altitude_ft = max(record.altitude_ft for record in telemetry_records)
    max_ground_speed_kts = max(record.ground_speed_kts for record in telemetry_records)
    highest_engine_temp_c = max(record.engine_temp_c for record in telemetry_records)
    fuel_used_percentage = first_record.fuel_percentage - last_record.fuel_percentage

    # Determine the outcome of the flight
    phases = [record.flight_phase for record in telemetry_records]

    if "crashed" in phases:
        outcome = "crashed"
    elif "landed" in phases:
        outcome = "landed"
    else:
        outcome = "incomplete"

    # Return the flight summary response
    return FlightSummaryResponse(
        flight_id=flight.id,
        flight_number=flight.flight_number,
        departure_airport=flight.departure_airport,
        arrival_airport=flight.arrival_airport,
        status=flight.status,
        duration_seconds=duration_seconds,
        telemetry_records=len(telemetry_records),
        max_altitude_ft=max_altitude_ft,
        max_ground_speed_kts=max_ground_speed_kts,
        fuel_used_percentage=fuel_used_percentage,
        highest_engine_temp_c=highest_engine_temp_c,
        alerts_generated=alerts_count,
        outcome=outcome
    )