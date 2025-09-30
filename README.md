# 🌐 API Guardian - AI Based Latency Prediction and Anomaly Detection

API Guardian is an AI-driven monitoring system that observes the `/hello` endpoint of a Spring Boot application behind Kong API Gateway. It predicts latency, detects anomalies, and provides a real-time dashboard for visualization.

**This project is submitted as part of [Kong-quer the Agentic AI hackathon 2025](https://konghq.com/events/conferences/api-summit/hackathon)**

---

## 🎯 Project Overview

This project monitors APIs behind Kong Gateway. Key features:

- Continuous monitoring of API endpoints
- Latency prediction using AI (Prophet Time-Series Forecasting Model)
- Anomaly detection for latency spikes and error rate
- Real-time visualization via Streamlit dashboard
- Stores metrics in a local SQLite database for persistence

The system acts like an **AI agent** by autonomously observing endpoints, predicting expected metrics, and highlighting anomalies.

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Kong API Gateway** (proxy management)
- **SQLite** (metrics storage)
- **Prophet Time-Series Forecasting Model** (latency prediction)
- **Pandas** (data manipulation)
- **Streamlit + Altair** (dashboard visualization)
- **Requests** (API checks)

---

## 📂 Project Structure

```

api-guardian/
├── .idea/                                               # IntelliJ IDEA project settings
├── spring-app/                                          # Spring Boot microservice
│   ├── pom.xml                                          # Maven project configuration
│   ├── Dockerfile                                       # Builds Docker image for Spring Boot API service
│   └── src/
│       └── main/
│           ├── java/
│           │   └── com/
│           │       └── example/
│           │           └── demo/
│           │               ├── Application.java         # Spring Boot main class
│           │               └── HelloController.java     # REST controller (/hello)
│           └── resources/
│               ├── application.properties               # Spring Boot config
├── .gitignore                                           # Git ignore rules
├── README.md                                            # Project documentation
├── ai_monitor.py                                        # ML model monitoring (Prophet for anomaly detection)
├── api-guardian.iml                                     # IntelliJ module file
├── dashboard.py                                         # Streamlit dashboard for monitoring results
├── docker-compose.yml                                   # Multi-service Docker setup
├── endpoint_logs.csv                                    # API request logs (CSV format)
├── init_db.py                                           # Script to initialize SQLite databases
├── metrics.db                                           # SQLite database for metrics
├── monitoring.db                                        # SQLite database for monitoring/anomaly detection
└── requirements.txt                                     # Python dependencies

```

---

## ⚙️ Local Setup with Kong

1. **Run Spring Boot Application**  
   Make sure your Spring Boot app is running on port `8080` and exposes `/hello` endpoint:

   ```bash
   git clone https://github.com/vishalpatil1202/api-guardian
   cd api-guardian/spring-app
   mvn spring-boot:run

2. **Start all services**
  
    ```bash
    docker-compose up -d

3. **Check running containers**

   ```bash
    docker ps
   ```

   You should see something like:
   
   | Container  | Port(s)    |
   | ---------- | ---------- |
   | kong       | 8000, 8001 |
   | spring-app | 8080       |
   | postgres   | 5432       |


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
    ```
    If everything is working, you should get the Spring app’s response, e.g.:
    ```
    {
    "message": "Hello from Spring App!"
    }
    ```
   
---

## 🚀 Setup & Running Locally

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
   
   ```bash
   python ai_monitor.py
   ```
   - Continuously monitors `/hello` endpoint via Kong
   - Logs timestamp, status, latency, predicted latency, anomaly flags

5. **Start Dashboard**
   
   ```bash
   streamlit run dashboard.py
   ```
   - Displays latency (actual vs predicted)
   - Shows anomaly rate over time
   - Shows latest check summary
   - Auto-refresh interval can be adjusted from the sidebar

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

## ✨ Future Improvements

- Add Slack/Email alerting for anomalies
- Extend to multiple endpoints automatically
- Predict error rates per endpoint

## ▶️ Demo Video 
🔗 https://youtu.be/KaR9GYVg6fI?si=l6urezDB3G8h5Mh3


  



    
    



