import sqlite3

DB_NAME = "metrics.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create metrics table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        timestamp TEXT PRIMARY KEY,
        route TEXT,
        status INTEGER,
        latency REAL,
        anomaly INTEGER,
        error_flag INTEGER,
        predicted_latency REAL,
        predicted_errors REAL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

if __name__ == "__main__":
    init_db()
