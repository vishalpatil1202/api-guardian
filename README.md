# 🌐 API Guardian

**AI-Based API Monitoring and Anomaly Detection Dashboard**

API Guardian is an AI-driven monitoring system that observes the `/hello` endpoint of a Spring Boot application behind Kong API Gateway. It predicts latency, detects anomalies, and provides a real-time dashboard for visualization.

---

## 🎯 Project Overview

This project monitors APIs behind Kong Gateway. Key features:

✅ Multilingual UI (supports 9 Indian languages)  
✅ Dynamic form for farmer details  
✅ Streamlit-based frontend  
✅ Colab notebook for reproducibility  
✅ Uses Gemma LLM to recommend real-world applicable schemes

✅ Continuous monitoring of API endpoints
✅ Latency prediction using AI (Prophet)
✅ Anomaly detection for latency spikes and error rate
✅ Real-time visualization via Streamlit dashboard
✅ Stores metrics in a local SQLite database for persistence

The system acts like an **AI agent** by autonomously observing endpoints, predicting expected metrics, and highlighting anomalies.

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Kong API Gateway** (proxy management)
- **SQLite** (metrics storage)
- **Prophet** (latency prediction)
- **Pandas** (data manipulation)
- **Streamlit + Altair** (dashboard visualization)
- **Requests** (API checks)

---

## 📂 Project Structure

```

api-guardian/
├── app.py # Streamlit frontend
├── gemma.py # Gemma model loading and response generation
├── requirements.txt # Dependencies
├── AgroSathi.ipynb # Google colab notebook
├── .gitignore
└── README.md

```

---

## 🚀 Local Setup with Kong

1. **Run Spring Boot Application**  
   Make sure your Spring Boot app is running on port `8080` and exposes `/hello` endpoint:

   ```bash
   ./mvnw spring-boot:run

2. **Run Kong Gateway**
   Start Kong (Docker example):

    ```bash
    docker run -d --name kong \
    -e KONG_DATABASE=off \
    -e KONG_PROXY_ACCESS_LOG=/dev/stdout \
    -e KONG_ADMIN_ACCESS_LOG=/dev/stdout \
    -e KONG_PROXY_ERROR_LOG=/dev/stderr \
    -e KONG_ADMIN_ERROR_LOG=/dev/stderr \
    -e KONG_ADMIN_LISTEN=0.0.0.0:8001 \
    -p 8000:8000 \
    -p 8001:8001 \
    kong:latest
   
3. **Add Service & Route in Kong**
    
    ```bash
    # Add service
    curl -i -X POST http://localhost:8001/services \
    --data "name=spring-app" \
    --data "url=http://host.docker.internal:8080"

    # Add route
    curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/hello" \
    --data "service.name=spring-app" \
    --data "strip_path=false"
   
4. **Test the Kong proxy**
    
    ```bash
   curl http://localhost:8000/hello
   
---

## ⚙️ Setup & Running Locally

1. **Clone the repo**
    
    ```bash
    git clone https://github.com/vishalpatil1202/api-guardian
    cd api-guardian
   
2. **Install Python dependencies**

    ```bash
   pip install -r requirements.txt

3. **Initialize Database**

    ```bash
   python init_db.py

4. **Start AI Monitoring Agent**
   - Continuously monitors /hello endpoint via Kong
   - Logs timestamp, status, latency, predicted latency, anomaly flags

    ```bash
   python ai_monitor.py

5. **Start Dashboard**
   - Displays latency (actual vs predicted)
   - Shows anomaly rate over time
   - Shows latest check summary
   - Auto-refresh interval can be adjusted from the sidebar

    ```bash
   pip install -r requirements.txt   
   
---

## 🧠 How AI Works

1. **Latency Prediction**
    - Uses Prophet time series model to forecast expected latency for the next API call.

2. **Anomaly Detection**
    - Latency anomalies: actual latency > predicted + threshold
    - Error anomalies: observed error rate > predicted + threshold
    - Flags anomalies for dashboard visualization

3. **Dashboard Visualization**
    - Latency vs Predicted Latency
    - Anomaly Rate
    - Latest API status & anomaly flag

---

## **Future Improvements**

- Add Slack/Email alerting for anomalies
- Extend to multiple endpoints automatically
- Predict error rates per endpoint


  



    
    



