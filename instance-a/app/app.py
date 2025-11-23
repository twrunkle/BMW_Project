from flask import Flask, render_template, jsonify
import json
import os
import requests
import threading
import time

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'latest.json')

# -----------------------------
# Backend URL (FastAPI container)
# If on same Docker network, use the container name
BACKEND_URL = "http://backend_web:8000/telemetry"
# If sending from outside Docker, use host IP instead:
# BACKEND_URL = "http://<backend_host_ip>:8000/telemetry"
# -----------------------------

def send_to_backend():
    """Send telemetry to the backend every few seconds."""
    while True:
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            response = requests.post(BACKEND_URL, json=data)
            if response.status_code != 200:
                print(f"Backend error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error sending to backend: {e}")
        time.sleep(5)  # adjust frequency as needed

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/raw')
def raw_data():
    return render_template('index.html')
@app.route('/data')
def get_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        data = {"error": str(e)}
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    # Start background thread to send data to backend
    threading.Thread(target=send_to_backend, daemon=True).start()
    app.run(host='0.0.0.0', port=9000)
