import time
import random
import requests
from datetime import datetime

# Constants
API_URL = "http://127.0.0.1:8000/telemetry/"

FLIGHT_ID = 1

FAULT_CHANCE = 0.10  # 10% chance to trigger a fault

FORCED_FAULT = "rapid_altitude_loss"  # Set to "engine_overheat", "fuel_leak", or "rapid_altitude_loss" to force a specific fault



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
                f"Fuel: {data['fuel_percentage']:.1f}% | "
                f"Engine Temp: {data['engine_temp_c']:.1f}°C"


            )



        else:
            print("Failed to send telemetry")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    
    # Handle connection errors
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

# Function to run the telemetry simulator
def run_simulator():

    altitude_ft = 0
    ground_speed_kts = 0
    fuel_percentage = 100
    engine_temp_c = 450

    # Fault variables
    active_fault = None  
    fault_triggered = False

    start_time = time.time()

    print("Starting telemetry simulator...")

    while True:
        
        # Simulate telemetry data
        elapsed_seconds = time.time() - start_time

        # TAXI 
        if elapsed_seconds < 20:
            flight_phase = "taxi"

            altitude_ft = 0
            ground_speed_kts = min(25, ground_speed_kts + random.uniform(1, 3))
            engine_temp_c += random.uniform(1, 3)
            fuel_percentage -= random.uniform(0.01, 0.03)

        # TAKEOFF
        elif elapsed_seconds < 35:
            flight_phase = "takeoff"

            altitude_ft += random.uniform(200, 400)
            ground_speed_kts = min(150, ground_speed_kts + random.uniform(15, 25))
            engine_temp_c += random.uniform(3, 6)
            fuel_percentage -= random.uniform(0.05, 0.09)

        # CLIMB
        elif altitude_ft < 35000 and elapsed_seconds < 100:
            flight_phase = "climb"

            altitude_ft += random.uniform(400, 700)
            ground_speed_kts = min(320, ground_speed_kts + random.uniform(2, 5))
            engine_temp_c += random.uniform(-1, 2)
            fuel_percentage -= random.uniform(0.03, 0.06)

        # CRUISE
        elif elapsed_seconds < 180:
            flight_phase = "cruise"

            altitude_ft = 35000 + random.uniform(-80, 80)
            ground_speed_kts = 455 + random.uniform(-5, 5)
            engine_temp_c = 720 + random.uniform(-10, 10)
            fuel_percentage -= random.uniform(0.02, 0.04)

        # DESCENT
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

        # LANDING
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
                
        if not fault_triggered and flight_phase in ["climb", "cruise"]:

            if FORCED_FAULT is not None:
                active_fault = FORCED_FAULT
                fault_triggered = True
                print(f"FORCED FAULT INJECTED: {active_fault}")

            elif random.random() < FAULT_CHANCE:  # Chance to trigger a fault
                active_fault = random.choice([
                    "engine_overheat", 
                    "fuel_leak",
                    "rapid_altitude_loss"
                ])
                
                fault_triggered = True
                print(f"FAULT INJECTED: {active_fault}")

        # Simulate fault conditions
        if active_fault == "engine_overheat":
            engine_temp_c += random.uniform(20, 40)  # Rapid increase in engine temperature

            ground_speed_kts -= random.uniform(2, 5)  # Decrease in speed due to engine issues

            if flight_phase == "climb":
                altitude_ft -= random.uniform(100, 250)  # Slower climb rate

            if engine_temp_c >= 930:
                flight_phase = "emergency_descent"
                altitude_ft -= random.uniform(500, 900)  # Rapid decrease in altitude
                ground_speed_kts = max(220, ground_speed_kts - random.uniform(5, 10))  # Increase in speed during descent

        elif active_fault == "fuel_leak":
            fuel_percentage -= random.uniform(0.8, 1.5)  # Rapid decrease in fuel level

        elif active_fault == "rapid_altitude_loss":
            flight_phase = "emergency_descent"
            altitude_ft -= random.uniform(1500, 2500)  # Rapid decrease in altitude
            ground_speed_kts = max(220, ground_speed_kts - random.uniform(5, 10))  # Increase in speed during descent
            altitude_ft = max(0, altitude_ft)  # Ensure altitude doesn't go below 0

        altitude_ft = max(0, altitude_ft)  # Ensure altitude doesn't go below 0
        ground_speed_kts = max(0, ground_speed_kts)  # Ensure speed doesn't go below 0
        engine_temp_c = max(0, engine_temp_c) # Ensure engine temperature doesn't go below 0
        fuel_percentage = max(0, fuel_percentage)  # Ensure fuel percentage doesn't go below 0
        
        if altitude_ft == 0 and active_fault is not None and flight_phase!= "landed":
            flight_phase = "crashed"
            ground_speed_kts = 0

        
        if flight_phase == "crashed":
            telemetry = {
                "flight_id": FLIGHT_ID,
                "timestamp": datetime.utcnow().isoformat(),
                "flight_phase": flight_phase,
                "altitude_ft": altitude_ft,
                "ground_speed_kts": ground_speed_kts,
                "fuel_percentage": fuel_percentage,
                "engine_temp_c": engine_temp_c  
            }

        # Create telemetry data dictionary
        telemetry = {
            "flight_id": FLIGHT_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "flight_phase": flight_phase,
            "altitude_ft": altitude_ft,
            "ground_speed_kts": ground_speed_kts,
            "fuel_percentage": fuel_percentage,
            "engine_temp_c": engine_temp_c
        
        }
        
        # Send telemetry data to the API
        send_telemetry(telemetry)
        
        time.sleep(1)  # Send telemetry data every second


if __name__ == "__main__":
    run_simulator()