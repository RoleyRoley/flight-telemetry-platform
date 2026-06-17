import time
import random
import requests
from datetime import datetime

# Constants
API_URL = "http://127.0.0.1:8000/telemetry/"

FLIGHT_ID = 1

# Function to generate random telemetry data
def generate_telemetry():
    telemetry = {
        "flight_id": FLIGHT_ID,
        "timestamp": datetime.now().isoformat(),
        "altitude_ft": random.uniform(10000, 12000),
        "ground_speed_kts": random.uniform(280, 320),
        "fuel_percentage": random.uniform(75, 85),
        "engine_temp_c": random.uniform(650, 750),
        "flight_phase": "climb"
    }
    return telemetry

# Function to send telemetry data to the API
def send_telemetry(data):
    try:
        response = requests.post(API_URL, json=data)

        # Check the response status code
        # 200 indicates success, while other codes indicate failure
        if response.status_code == 200:
            print("Telemetry data sent successfully.", response.json())
        else:
            print("Failed to send telemetry")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    
    # Handle connection errors
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

# Function to run the telemetry simulator
def run_simulatior():
    print("Starting telemetry simulator...")

    while True:
        telemetry = generate_telemetry()
        send_telemetry(telemetry)
        time.sleep(5)  # Send telemetry data every 5 seconds


if __name__ == "__main__":
    run_simulatior()