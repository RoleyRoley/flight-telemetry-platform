from fastapi import APIRouter

router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"],
)

# Check if the telemetry endpoint is working
@router.post("/")
def create_telemetry():
    return {"message": "Telemetry recieved."}