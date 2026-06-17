import time
import random
import requests
from datetime import datetime

# Constants
API_URL = "http://127.0.0.1:8000/telemetry/"

FLIGHT_ID = 1






# Function to send telemetry data to the API
def send_telemetry(data):
    try:
        response = requests.post(API_URL, json=data)

        # Check the response status code
        # 200 indicates success, while other codes indicate failure
        if response.status_code == 200:
            print(
                f"{data['flight_phase'].upper()} | "
                f"Alt {data['altitude_ft']:.0f} ft | "
                f"Speed: {data['ground_speed_kts']:.0f} kts | "
                f"Fuel: {data['fuel_percentage']:.1f}%"


            )



        else:
            print("Failed to send telemetry")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    
    # Handle connection errors
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

# Function to run the telemetry simulator
def run_simulatior():

    altitude_ft = 0
    ground_speed_kts = 0
    fuel_percentage = 100
    engine_temp_c = 450

    start_time = time.time()

    print("Starting telemetry simulator...")

    while True:
        
        # Simulate telemetry data
        elapsed_seconds = time.time() - start_time

        if elapsed_seconds< 20:
            flight_phase = "taxi"

            altitude_ft = 0
            ground_speed_kts += random.uniform(2, 5)
            engine_temp_c += random.uniform(1, 3)
            fuel_percentage -= random.uniform(0.01, 0.03)

        elif elapsed_seconds < 40:
            flight_phase = "takeoff"

            altitude_ft += random.uniform(200, 400)
            ground_speed_kts += random.uniform(15, 25)
            engine_temp_c += random.uniform(3, 6)
            fuel_percentage -= random.uniform(0.05, 0.09)

        elif altitude_ft < 35000 and elapsed_seconds < 140:
            flight_phase = "climb"

            altitude_ft += random.uniform(400, 700)
            ground_speed_kts += random.uniform(3, 6)
            engine_temp_c += random.uniform(-1, 2)
            fuel_percentage -= random.uniform(0.03, 0.06)

        elif elapsed_seconds < 220:
            flight_phase = "cruise"

            altitude_ft = 35000 + random.uniform(-80, 80)
            ground_speed_kts = 455 + random.uniform(-5, 5)
            engine_temp_c = 720 + random.uniform(-10, 10)
            fuel_percentage -= random.uniform(0.02, 0.04)

        elif altitude_ft > 0:
            flight_phase = "descent"

            altitude_ft -= random.uniform(500, 800)
            ground_speed_kts -= random.uniform(1, 4)
            engine_temp_c -= random.uniform(1, 3)
            fuel_percentage -= random.uniform(0.01, 0.03)

            if altitude_ft < 0:
                altitude_ft = 0

            if ground_speed_kts < 0:
                ground_speed_kts = 0
    
        else:
                flight_phase = "landed"

                altitude_ft = 0
                ground_speed_kts = 0

                telemetry = {
                    "flight_id": FLIGHT_ID,
                    "timestamp": datetime.utcnow().isoformat(),
                    "flight_phase": flight_phase,
                    "altitude_ft": altitude_ft,
                    "ground_speed_kts": ground_speed_kts,
                    "fuel_percentage": fuel_percentage,
                    "engine_temp_c": engine_temp_c  
                }

                send_telemetry(telemetry)
                print("Flight simulation complete.")
                break
                
        telemetry = {
            "flight_id": FLIGHT_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "flight_phase": flight_phase,
            "altitude_ft": altitude_ft,
            "ground_speed_kts": ground_speed_kts,
            "fuel_percentage": fuel_percentage,
            "engine_temp_c": engine_temp_c

        }
        
        send_telemetry(telemetry)
        
        time.sleep(5)  # Send telemetry data every 5 seconds


if __name__ == "__main__":
    run_simulatior()