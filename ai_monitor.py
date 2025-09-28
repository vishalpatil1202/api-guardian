import requests
import sqlite3
import time
from datetime import datetime
import pandas as pd
from prophet import Prophet
import numpy as np

DB_NAME = "metrics.db"
ROUTE = "/hello"
URL = f"http://localhost:8000{ROUTE}"  # Kong proxy URL
INTERVAL = 10  # seconds
THRESHOLD_LATENCY = 0.5  # seconds
THRESHOLD_ERROR = 0.1   # for error rate anomalies

# Initialize DB
from init_db import init_db
init_db()

def log_metric(timestamp, route, status, latency, anomaly, error_flag, predicted_latency, predicted_errors):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO metrics 
        (timestamp, route, status, latency, anomaly, error_flag, predicted_latency, predicted_errors)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, route, status, latency, int(anomaly), error_flag, predicted_latency, predicted_errors))
    conn.commit()
    conn.close()

def forecast_metric(df, column):
    """Forecast the next value using Prophet."""
    if len(df) < 2:
        return None  # not enough data to predict

    temp = df[['timestamp', column]].copy()
    temp.rename(columns={'timestamp':'ds', column:'y'}, inplace=True)
    try:
        model = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
        model.fit(temp)
        future = model.make_future_dataframe(periods=1, freq='S')
        forecast = model.predict(future)
        return float(forecast['yhat'].iloc[-1])
    except Exception as e:
        print("⚠ Forecast error:", e)
        return None

def check_endpoint():
    try:
        start = time.time()
        resp = requests.get(URL)
        latency = time.time() - start
        status = resp.status_code
        error_flag = 1 if status >= 400 else 0
    except Exception as e:
        print("❌ Request failed:", e)
        latency = None
        status = 0
        error_flag = 1

    # Load historical data for predictions
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM metrics ORDER BY timestamp ASC", conn)
    conn.close()

    predicted_latency = forecast_metric(df, 'latency')
    predicted_errors = forecast_metric(df, 'error_flag')

    # Determine anomaly
    anomaly_latency = predicted_latency is not None and latency is not None and latency > predicted_latency + THRESHOLD_LATENCY
    anomaly_error = predicted_errors is not None and error_flag > predicted_errors + THRESHOLD_ERROR
    anomaly = anomaly_latency or anomaly_error

    timestamp = datetime.utcnow().isoformat()
    log_metric(timestamp, ROUTE, status, latency or 0.0, anomaly, error_flag, predicted_latency or 0.0, predicted_errors or 0.0)

    print(f"{'🚨' if anomaly else '✅'} {timestamp} | {ROUTE} | Status: {status} | Latency: {latency:.3f}s | Anomaly: {anomaly}")

if __name__ == "__main__":
    print("🤖 Starting API Guardian Agent...")
    while True:
        check_endpoint()
        time.sleep(INTERVAL)
