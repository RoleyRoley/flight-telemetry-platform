from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TelemetryRecord, Alert, Flight
from app.services.anomaly_detector import detect_alerts
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
        flight_phase=telemetry.flight_phase,
        latitude=telemetry.latitude,
        longitude=telemetry.longitude,
        heading_deg=telemetry.heading_deg,
        route_progress_percentage=telemetry.route_progress_percentage
    )

    # Add the new telemetry record to the database
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    
    flight = (
    db.query(Flight)
    .filter(Flight.id == new_record.flight_id)
    .first()
    )

    if flight:
        if new_record.flight_phase in ["taxi", "takeoff", "climb", "cruise", "descent", "emergency_descent"]:
            flight.status = "in_flight"

        elif new_record.flight_phase == "landed":
            flight.status = "landed"

        elif new_record.flight_phase == "crashed":
            flight.status = "crashed"

        db.commit()

    
    # Detect alerts based on the new telemetry record
    generated_alerts = detect_alerts(new_record)

    created_alerts = 0

    for alert_data in generated_alerts:

        exisiting_alert = (
            db.query(Alert)
            .filter(
                Alert.flight_id == new_record.flight_id,
                Alert.alert_type == alert_data["alert_type"]
            )
            .first()
        )

        if exisiting_alert:
            continue





        alert = Alert(
            flight_id=new_record.flight_id,
            telemetry_record_id=new_record.id,
            timestamp=new_record.timestamp,
            alert_type=alert_data["alert_type"],
            severity=alert_data["severity"],
            message=alert_data["message"]
        )
        db.add(alert)

        created_alerts += 1

    # Commit the alerts to the database if any were generated
    if created_alerts > 0:
        db.commit()

    return {
        "message": "Telemetry record created successfully.",
        "record_id": new_record.id,
        "alerts_generated": len(generated_alerts),   
        "alerts_created": created_alerts
        }

# Get the latest telemetry record
@router.get("/latest")
def get_latest_telemetry(db: Session = Depends(get_db)):
    latest = (
        db.query(TelemetryRecord)
        .order_by(TelemetryRecord.timestamp.desc())
        .first()
    )
    
    if latest is None:
        return None
    
    return latest