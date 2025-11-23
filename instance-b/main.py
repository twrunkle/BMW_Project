from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import psycopg2
import json
import os
from datetime import datetime

app = FastAPI()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'telemetry-db'),  # Use container name if on same Docker network
    'dbname': os.getenv('DB_NAME', 'telemetry_data'),
    'user': os.getenv('DB_USER', 'telemetry_backend'),
    'password': os.getenv('DB_PASS', 'password'),
    'port': 5432
}

# Pydantic model
class Telemetry(BaseModel):
    car_id: int
    speed: float
    rpm: int
    throttle: float
    engine_temp: float

# Function to insert telemetry into DB
def insert_telemetry(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Ensure table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_table (
                id SERIAL PRIMARY KEY,
                payload JSONB NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        # Insert data
        cur.execute(
            "INSERT INTO telemetry_table (payload, created_at) VALUES (%s, %s);",
            [json.dumps(data), datetime.now()]
        )
        conn.commit()
    except Exception as e:
        print(f"[DB ERROR] Failed to insert telemetry: {e}")
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

# Function to fetch recent inserts
def get_recent_inserts(limit=10):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, payload, created_at FROM telemetry_table ORDER BY created_at DESC LIMIT %s;",
            (limit,)
        )
        rows = cur.fetchall()
        return [{"id": r[0], "payload": r[1], "created_at": r[2].isoformat()} for r in rows]
    except Exception as e:
        print(f"[DB ERROR] Failed to fetch recent inserts: {e}")
        return []
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

# Endpoint to receive telemetry
@app.post("/data")
def receive_telemetry(payload: List[Telemetry]):
    inserted = 0
    for item in payload:
        insert_telemetry(item.dict())
        inserted += 1
    return {"status": "success", "inserted": inserted}

# Endpoint to view recent inserts
@app.get("/recent")
def recent_telemetry(limit: int = 10):
    recent_data = get_recent_inserts(limit)
    return {"recent_inserts": recent_data}
