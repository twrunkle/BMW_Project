from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import psycopg2
import json
import os
from datetime import datetime

app = FastAPI()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'telemetry_data'),
    'user': os.getenv('DB_USER', 'telemetry_backend'),
    'password': os.getenv('DB_PASS', 'password'),
    'port': 5432
}

class Telemetry(BaseModel):
    car_id: int
    speed: float
    rpm: int
    throttle: float
    engine_temp: float

def insert_telemetry(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_table (
            id SERIAL PRIMARY KEY,
            payload JSONB NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """)
    cur.execute(
        "INSERT INTO telemetry_table (payload, created_at) VALUES (%s, %s);",
        [json.dumps(data), datetime.now()]
    )
    conn.commit()
    cur.close()
    conn.close()

@app.post("/data")
def receive_telemetry(payload: List[Telemetry]):
    for item in payload:
        insert_telemetry(item.dict())
    return {"status": "success", "inserted": len(payload)}
