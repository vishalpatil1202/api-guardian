import streamlit as st
import pandas as pd
import sqlite3
import time
import altair as alt

DB_NAME = "metrics.db"

# Load metrics data
def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM metrics ORDER BY timestamp ASC", conn)
    conn.close()
    return df

st.set_page_config(page_title="API Guardian Dashboard", layout="wide")
st.title("🌐 API Monitoring Dashboard")
st.markdown("Monitoring `/hello` endpoint behind Kong")

refresh_rate = st.sidebar.slider("⏱ Refresh every (seconds)", 5, 60, 10)
placeholder = st.empty()

while True:
    df = load_data()

    if df.empty:
        st.warning("⚠ No data yet. Please start `ai_monitor.py` to collect metrics.")
        time.sleep(refresh_rate)
        continue

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    with placeholder.container():
        st.subheader("📊 Latency Overview")
        # Melt dataframe to show actual vs predicted latency with legend
        df_latency = df.melt(
            id_vars=["timestamp"],
            value_vars=["latency", "predicted_latency"],
            var_name="Type",
            value_name="Value"
        )
        latency_chart = alt.Chart(df_latency).mark_line(point=True).encode(
            x="timestamp:T",
            y=alt.Y("Value:Q", title="Latency (s)"),
            color=alt.Color("Type:N", legend=alt.Legend(title="Latency Type")),
            tooltip=["timestamp", "Type", "Value"]
        ).properties(width=800, height=400)
        st.altair_chart(latency_chart, use_container_width=True)

        # Anomaly Rate Chart
        st.subheader("🚨 Anomaly Rate Over Time")
        df_anomaly = df.set_index("timestamp").resample("1T")["anomaly"].mean().reset_index()  # 1-minute resample
        anomaly_chart = alt.Chart(df_anomaly).mark_line(point=True, color="red").encode(
            x="timestamp:T",
            y=alt.Y("anomaly:Q", title="Anomaly Rate"),
            tooltip=["timestamp", alt.Tooltip("anomaly:Q", title="Anomaly Rate")]
        ).properties(width=800, height=200)
        st.altair_chart(anomaly_chart, use_container_width=True)

        # Latest Check
        latest = df.iloc[-1]
        st.subheader("🟢 Latest Check")
        st.write(f"**Route**: {latest['route']}")
        st.write(f"**Status**: {latest['status']}")
        st.write(f"**Latency**: {latest['latency']:.3f}s")
        if latest["predicted_latency"] is not None:
            st.write(f"**Predicted Latency**: {latest['predicted_latency']:.3f}s")
        st.write(f"**Anomaly**: {'🚨 YES' if latest['anomaly'] else '✅ NO'}")

    time.sleep(refresh_rate)
