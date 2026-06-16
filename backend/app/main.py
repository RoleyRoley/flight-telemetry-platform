from fastapi import FastAPI, HTTPException

# TEST ======
from app.database import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Flight Telemetry Platform API",
    description="API for managing flight telemetry data and related operations.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Flight Telemetry API is running.",
        "docs": "/docs",
        "health": "/health",
        "details": "/details",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Flight Telemetry API is running."
}


@app.get("/details")
def details():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
        "health": "/health",
    }



# TEST ======




@app.get("/db-test")
def test_database():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))

            return {
                "database": "connected",
                "result": result.scalar(),
            }
    except SQLAlchemyError as exc:
        error_detail = str(getattr(exc, "orig", exc))
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {error_detail}",
        ) from exc