import json
import random
import time
import os
import requests

# Ensure the data folder exists
os.makedirs('data', exist_ok=True)

# Backend endpoint
backend_url = 'http://172.31.29.117:8000/data'  # Your FastAPI backend private IP

while True:
    # Generate telemetry
    data = [{
        "car_id": 1,
        "speed": random.uniform(0, 120),
        "rpm": random.randint(1000, 5000),
        "throttle": random.uniform(0, 100),
        "engine_temp": random.uniform(70, 120)
    }]

    # Send data to backend
    try:
        response = requests.post(backend_url, json=data)
        print(f"Sent to backend: {data}, response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send to backend: {e}")

    # Write data to local JSON for Flask webpage
    try:
        with open('data/latest.json', 'w') as f:
            json.dump(data[0], f)  # Save single telemetry entry for webpage
        print("Updated data/latest.json for webpage")
    except Exception as e:
        print(f"Failed to write latest.json: {e}")

    time.sleep(2)
