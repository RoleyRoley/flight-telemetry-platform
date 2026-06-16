from fastapi import FastAPI

app = FastAPI(
    title="Flight Telemetry Platform API",
    description="API for managing flight telemetry data and related operations.",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


