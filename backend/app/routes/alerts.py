from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert
from app.schemas import AlertResponse

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)

# Get all alerts
@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    alerts = (
        db.query(Alert)
        .order_by(Alert.timestamp.desc())
        .all()
    )
    return alerts

# Get alerts for a specific flight
@router.get("/flight/{flight_id}", response_model=list[AlertResponse])
def get_alerts_by_flight( 

    flight_id: int, 
    db: Session = Depends(get_db)

    ):

    # Query the database for alerts associated with the specified flight ID, ordered by timestamp in descending order
    alerts = (
        db.query(Alert)
        .filter(Alert.flight_id == flight_id)
        .order_by(Alert.timestamp.desc())
        .all()
    )
    return alerts