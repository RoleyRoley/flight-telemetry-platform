from app.models import Alert


# Function to detect alerts based on telemetry data
def detect_alerts(telemetry_record):
    alerts = []

    # Check for engine temperature anomalies
    if telemetry_record.engine_temp_c > 880:
        alerts.append({
            "alert_type": "engine_overheat_warning",
            "severity": "warning",
            "message": "Engine temperature approaching high threshold."
        })

    elif telemetry_record.engine_temp_c > 900:
        alerts.append({
            "alert_type": "engine_overheat_critical",
            "severity": "critical",
            "message": "Engine temperature exceeded safe operating limits."
        })
    
    # Check for fuel level anomalies
    if telemetry_record.fuel_percentage < 20:
        alerts.append({
            "alert_type": "fuel_low_warning",
            "severity": "warning",
            "message": "Fuel level low: below 20%."
        })
    
    elif telemetry_record.fuel_percentage < 10:
        alerts.append({
            "alert_type": "fuel_low_critical",
            "severity": "critical",
            "message": "Fuel level critically low: below 10%."
        })

    # Check for altitude anomalies
    if telemetry_record.altitude_ft > 41000:
        alerts.append({
            "alert_type": "altitude_high_warning",
            "severity": "warning",
            "message": "Altitude exceeds expected operating range."
        })
    
    if telemetry_record.flight_phase == "emergency_descent":
        alerts.append({
            "alert_type": "emergency_descent",
            "severity": "critical",
            "message": "Emergency descent detected."
        })

    if telemetry_record.flight_phase == "crashed":
        alerts.append({
            "alert_type": "crash_detected",
            "severity": "critical",
            "message": "Aircraft impact detected following active fault."
        })
    
    return alerts