# DigitalTwin.ai

> **AI-powered digital twin for predictive manufacturing operations**

DigitalTwin.ai is an intelligent manufacturing operations platform that combines a simulated production environment with machine learning and decision intelligence.

The system continuously monitors factory stations, detects anomalies and bottlenecks, estimates defect risk, identifies potential root causes, generates actionable recommendations, and allows operators to evaluate interventions through **what-if simulation** before applying them to the production line.

---

## 🚀 What Problem Does It Solve?

Manufacturing disruptions rarely happen because of a single isolated event.

A small change in machine behavior can create a chain reaction:

       Machine degradation
              ↓
       Cycle-time increase
              ↓
       Queue buildup
              ↓
       Bottleneck
              ↓
       Production risk
              ↓
       Potential quality issues

Traditional monitoring systems may identify that a station is abnormal, but the operator still needs to determine:

What is causing the problem?
How serious is it?
Which intervention should be performed?
What could happen downstream?
Is the proposed intervention actually beneficial?

DigitalTwin.ai closes this decision loop.

----

## 🧠 Core Concept

DigitalTwin.ai follows a closed operational intelligence loop:

       OBSERVE
         ↓
       DETECT
         ↓
       EXPLAIN
         ↓
       RECOMMEND
         ↓
       SIMULATE
         ↓
       DECIDE

Instead of stopping at anomaly detection, the platform moves from machine telemetry to operational decision support.

## ✨ Core Capabilities
### 🏭 Digital Factory Twin
       Simulated manufacturing stations
       Vehicles moving through the production line
       Buffers and queues
       Station health and operational state
       Live telemetry generation
### 🤖 Machine Learning
       Anomaly detection
       Bottleneck prediction
       Defect-risk prediction
       Live model inference
       Station-level risk scoring
### 🔎 Root Cause Intelligence
       Signal-based root-cause ranking
       Supporting evidence for each cause
       Severity and contribution scoring
       Identification of the dominant operational signals
### 💡 Recommendations
       Actionable station-level recommendations
       Priority levels
       Confidence scores
       Expected operational effects
### 🔮 What-If Simulation
       Test operational interventions virtually
       Compare baseline vs simulated state
       Estimate risk reduction
       Evaluate downstream effects
       Support operator decision-making before physical intervention
### 📊 Interactive Dashboard
       Live factory visualization
       Station intelligence
       KPI monitoring
       Risk visualization
       Root-cause analysis
       Recommendation panels
       Downstream impact visualization

## 🏗️ System Architecture
```
┌───────────────────────────────┐
│       Factory Simulation      │
│ Stations • Vehicles • Buffers │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Telemetry Generation     │
│ Cycle Time • Torque • Vibration│
│ Temperature • Queue • Sensors │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Digital Twin           │
│ Factory State + Live Events   │
└───────────────┬───────────────┘
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
   Anomaly  Bottleneck  Defect
  Detection Prediction  Risk
        │       │        │
        └───────┼────────┘
                ▼
┌───────────────────────────────┐
│         Risk Scoring          │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│      Root Cause Analysis      │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│       Recommendations         │
│ Action • Priority • Confidence│
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│       What-If Simulation      │
│ Baseline → Intervention       │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│      Downstream Impact        │
└───────────────┬───────────────┘
                ▼
        Operator Decision
```

## 📁 Project Structure

       DigitalTwin.ai/
       │
       ├── backend/
       │   │
       │   ├── app/
       │   │   ├── api/
       │   │   │   └── twin.py
       │   │   │
       │   │   ├── ml/
       │   │   │   ├── anomaly.py
       │   │   │   ├── bottleneck.py
       │   │   │   ├── defect.py
       │   │   │   ├── features.py
       │   │   │   ├── live_features.py
       │   │   │   ├── live_predictor.py
       │   │   │   ├── recommendation.py
       │   │   │   ├── risk_score.py
       │   │   │   └── root_cause.py
       │   │   │
       │   │   ├── simulation/
       │   │   │   ├── dataset.py
       │   │   │   ├── dynamics.py
       │   │   │   ├── generator.py
       │   │   │   ├── propagation.py
       │   │   │   ├── quality.py
       │   │   │   └── what_if.py
       │   │   │
       │   │   └── twin/
       │   │       ├── engine.py
       │   │       ├── factory.py
       │   │       ├── graph.py
       │   │       ├── manager.py
       │   │       ├── metrics.py
       │   │       ├── station.py
       │   │       └── vehicle.py
       │   │
       │   ├── main.py
       │   ├── requirements.txt
       │   │
       │   ├── generate_dataset.py
       │   ├── train_anomaly.py
       │   ├── train_bottleneck.py
       │   ├── train_defect.py
       │   │
       │   └── test_*.py
       │
       ├── frontend/
       │   ├── public/
       │   ├── src/
       │   │   ├── api/
       │   │   ├── assets/
       │   │   ├── App.jsx
       │   │   ├── App.css
       │   │   ├── index.css
       │   │   └── main.jsx
       │   ├── package.json
       │   └── vite.config.js
       │
       ├── .gitignore
       └── README.md


## ⚙️ Technology Stack
### Frontend
       React
       Vite
       JavaScript
       CSS
### Backend
       Python
       FastAPI
       Pandas
       NumPy
       Scikit-learn
### Intelligence Layer
       Anomaly detection
       Bottleneck prediction
       Defect-risk prediction
       Feature engineering
       Live inference
       Risk scoring
       Root-cause ranking
       Recommendation generation
       What-if simulation
## 🛠️ Local Setup
### 1. Clone the Repository
       git clone https://github.com/Aniket-8314/DigitalTwin.ai.git
       cd DigitalTwin.ai

### 2. Backend Setup

Open a terminal:

       cd backend

Create a Python virtual environment:

       python -m venv .venv

Activate it on Windows:

       .\.venv\Scripts\Activate.ps1

Install dependencies:

       pip install -r requirements.txt

Start the FastAPI backend:

       uvicorn main:app --reload

The backend will run at:

       http://127.0.0.1:8000

FastAPI documentation:

       http://127.0.0.1:8000/docs
       
### 3. Frontend Setup

Open another terminal:

       cd frontend

Install dependencies:

       npm install

Start the development server:

       npm run dev

Open the Vite development URL displayed in the terminal.

## 🔄 Demonstration Scenario

The primary demonstration scenario uses Station S14.

The simulation introduces a controlled degradation that propagates through the production line.
```
S14 Torque Drift
       ↓
Torque degradation
       ↓
Vibration increase
       ↓
Cycle-time increase
       ↓
Queue buildup
       ↓
Bottleneck detection
       ↓
Risk escalation
       ↓
Root-cause analysis
       ↓
AI recommendation
       ↓
What-if intervention
       ↓
Downstream impact
       ↓
Operator decision
```

## 🔮 What-If Decision Support

One of the key features of DigitalTwin.ai is the ability to evaluate an intervention before applying it to the physical production system.

For example:

       Current Station State
              ↓
           What-If
              ↓
       Speed Change = -3%
              ↓
       Virtual Simulation
              ↓
       Risk Comparison
              ↓
       Downstream Impact
              ↓
           Decision

The simulation provides:

       Baseline cycle time
       Simulated cycle time
       Baseline queue
       Simulated queue
       Baseline risk
       Simulated risk
       Downstream station impact
       Downstream health changes

This allows an operator to evaluate a proposed intervention using the digital twin before making a physical production change.

## 📡 API Overview

The backend exposes the following primary Digital Twin APIs:

       Endpoint	                     Purpose
       GET /api/twin/state	       Overall digital twin state
       GET /api/twin/metrics	Factory-level KPIs
       GET /api/twin/stations	Station telemetry and intelligence
       GET /api/twin/vehicles	Vehicle and defect information
       GET /api/twin/buffers	Buffer state
       GET /api/twin/graph	       Production process graph
       POST /api/twin/start	       Start simulation
       POST /api/twin/stop	       Stop simulation
       POST /api/twin/what-if	Run intervention simulation

Interactive API documentation is available through FastAPI Swagger:

       http://127.0.0.1:8000/docs

## 🧪 Testing

The backend contains test and validation scripts covering major components of the system.

Examples include:

       test_factory.py
       test_station.py
       test_vehicle.py
       test_telemetry.py
       test_processor.py
       test_propagation.py
       test_quality.py
       test_metrics.py
       test_twin.py
       test_graph.py

Model-related validation scripts are also included for:

       Anomaly Detection
       Bottleneck Prediction
       Defect Prediction
       Feature Engineering
       📈 Operational Intelligence Flow

DigitalTwin.ai transforms raw production telemetry into an operational decision:

       Raw Telemetry
       ↓
       Feature Engineering
       ↓
       ML Predictions
       ↓
       Risk Score
       ↓
       Root Causes
       ↓
       Recommendations
       ↓
       What-If Simulation
       ↓
       Downstream Impact
       ↓
       Decision

The goal is not simply to detect problems, but to help an operator understand and evaluate what to do next.

## 🎯 Project Status

Prototype completed for the Accenture Innovation Challenge 2026.

The current implementation demonstrates an end-to-end manufacturing digital-twin workflow covering:

       Factory simulation
       Live telemetry
       Machine learning inference
       Operational risk analysis
       Root-cause intelligence
       Recommendation generation
       What-if simulation
       Downstream impact analysis
       Interactive decision support

## 👥 Team

Built for the Accenture Innovation Challenge 2026.

### ⭐ If You Find This Project Interesting

DigitalTwin.ai demonstrates how digital twins, machine learning, and simulation can work together to support predictive and proactive manufacturing operations.