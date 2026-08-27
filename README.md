# DigitalTwin.ai

DigitalTwin.ai is an AI-powered digital twin for predictive manufacturing
operations. It combines a simulated production environment, live telemetry,
machine learning, root-cause analysis, recommendations, and what-if simulation
to help operators understand production risks and evaluate interventions before
applying them to the physical production line.

The system monitors manufacturing stations, vehicles, buffers, and production
signals such as cycle time, torque, vibration, temperature, and queue length.
It detects anomalies and bottlenecks, estimates defect risk, ranks potential
root causes, generates actionable recommendations, and evaluates operational
changes through digital-twin simulation.

This project was developed for the **Accenture Innovation Challenge 2026**.

## Table of contents

- [Requirements](#requirements)
- [Features](#features)
- [System architecture](#system-architecture)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the application](#running-the-application)
- [Demonstration scenario](#demonstration-scenario)
- [What-if simulation](#what-if-simulation)
- [API](#api)
- [Machine learning](#machine-learning)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Project status](#project-status)
- [Maintainers](#maintainers)

## Requirements

DigitalTwin.ai requires the following software:

- Python 3.10 or later
- Node.js and npm
- Git

The backend uses the following Python libraries:

- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- Joblib

The frontend uses:

- React
- Vite
- JavaScript
- CSS

The exact Python dependencies are listed in
[`backend/requirements.txt`](backend/requirements.txt).

The frontend dependencies are listed in
[`frontend/package.json`](frontend/package.json).

## Features

### Digital factory twin

- Simulated manufacturing stations
- Production vehicles
- Buffers and queues
- Station health monitoring
- Live telemetry generation
- Production-line process graph
- Factory-level operational metrics

### Machine learning

- Anomaly detection
- Bottleneck prediction
- Defect-risk prediction
- Live model inference
- Feature engineering
- Station-level risk scoring

### Root-cause intelligence

The system analyzes operational signals and ranks potential contributors
to station risk.

Supported signals include:

- Torque deviation
- Vibration increase
- Cycle-time deviation
- Queue buildup
- Temperature increase

Each root cause includes:

- Signal name
- Contribution score
- Direction
- Supporting evidence

### Recommendations

DigitalTwin.ai converts detected operational conditions into actionable
recommendations.

Recommendations include:

- Action
- Priority
- Reason
- Expected effect
- Confidence

### What-if simulation

Operators can test potential interventions against the digital twin before
making changes to the physical production line.

The simulation compares:

- Baseline cycle time
- Simulated cycle time
- Baseline queue
- Simulated queue
- Baseline temperature
- Simulated temperature
- Baseline vibration
- Simulated vibration
- Baseline torque
- Simulated torque
- Baseline risk
- Simulated risk

The system also estimates downstream impact on affected stations.

## System architecture

```text
                    ┌──────────────────────┐
                    │  Factory Simulation  │
                    │ Stations • Vehicles  │
                    │ Buffers • Queues     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Telemetry Generation │
                    │ Cycle Time           │
                    │ Torque               │
                    │ Vibration            │
                    │ Temperature          │
                    │ Queue Length         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Digital Twin     │
                    │ Factory State        │
                    │ Live Events          │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐   ┌────────────┐   ┌───────────┐
        │  Anomaly  │   │ Bottleneck │   │  Defect   │
        │ Detection │   │ Prediction │   │   Risk    │
        └─────┬─────┘   └──────┬─────┘   └─────┬─────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Risk Scoring     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Root Cause Analysis │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Recommendations    │
                    │ Action • Priority    │
                    │ Confidence           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  What-If Simulation  │
                    │ Baseline vs Scenario │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Downstream Impact   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Operator Decision  │
                    └──────────────────────┘

The overall decision-intelligence loop is:

       Observe
       ↓
       Detect
       ↓
       Explain
       ↓
       Recommend
       ↓
       Simulate
       ↓
       Decide
```
## Project structure
       DigitalTwin.ai/
       │
       ├── backend/
       │   │
       │   ├── app/
       │   │   │
       │   │   ├── api/
       │   │   │   └── twin.py
       │   │   │
       │   │   ├── ml/
       │   │   │   ├── anomaly.py
       │   │   │   ├── bottleneck.py
       │   │   │   ├── defect.py
       │   │   │   ├── defect_labels.py
       │   │   │   ├── defect_risk.py
       │   │   │   ├── features.py
       │   │   │   ├── history.py
       │   │   │   ├── impact.py
       │   │   │   ├── labels.py
       │   │   │   ├── live_features.py
       │   │   │   ├── live_predictor.py
       │   │   │   ├── recommendation.py
       │   │   │   ├── risk.py
       │   │   │   ├── risk_score.py
       │   │   │   └── root_cause.py
       │   │   │
       │   │   ├── simulation/
       │   │   │   ├── dataset.py
       │   │   │   ├── dynamics.py
       │   │   │   ├── generator.py
       │   │   │   ├── propagation.py
       │   │   │   ├── quality.py
       │   │   │   ├── stream.py
       │   │   │   ├── telemetry.py
       │   │   │   └── what_if.py
       │   │   │
       │   │   └── twin/
       │   │       ├── buffer.py
       │   │       ├── engine.py
       │   │       ├── event.py
       │   │       ├── factory.py
       │   │       ├── graph.py
       │   │       ├── graph_builder.py
       │   │       ├── manager.py
       │   │       ├── metrics.py
       │   │       ├── processor.py
       │   │       ├── quality.py
       │   │       ├── state.py
       │   │       ├── station.py
       │   │       └── vehicle.py
       │   │
       │   ├── main.py
       │   ├── requirements.txt
       │   │
       │   ├── generate_dataset.py
       │   ├── create_features.py
       │   ├── create_bottleneck_dataset.py
       │   ├── create_defect_dataset.py
       │   │
       │   ├── train_anomaly.py
       │   ├── train_bottleneck.py
       │   ├── train_defect.py
       │   │
       │   └── test_*.py
       │
       ├── frontend/
       │   │
       │   ├── public/
       │   ├── src/
       │   │   ├── api/
       │   │   ├── assets/
       │   │   ├── App.jsx
       │   │   ├── App.css
       │   │   ├── index.css
       │   │   └── main.jsx
       │   │
       │   ├── package.json
       │   ├── package-lock.json
       │   └── vite.config.js
       │
       ├── .gitignore
       └── README.md
## Installation
### 1. Clone the repository

Clone the repository from GitHub:

       git clone https://github.com/Aniket-8314/DigitalTwin.ai.git

       cd DigitalTwin.ai
### 2. Set up the backend

Navigate to the backend:

       cd backend

Create a Python virtual environment:

       python -m venv .venv

Activate the virtual environment on Windows:

       .\.venv\Scripts\Activate.ps1

Install the backend dependencies:

       pip install -r requirements.txt
### 3. Set up the frontend

Open another terminal and navigate to the frontend:

       cd frontend

Install the Node.js dependencies:

       npm install
Configuration

The frontend uses environment variables for the backend API configuration.

Create a local environment file:

       frontend/.env

Set the backend API URL according to your local environment:

       VITE_API_URL=http://127.0.0.1:8000

The repository's .gitignore excludes environment files from version control.

## Running the application

DigitalTwin.ai requires the backend and frontend to run simultaneously.

### Start the backend

From the backend directory:

       uvicorn main:app --reload

The backend will be available at:

       http://127.0.0.1:8000

FastAPI provides interactive API documentation at:

       http://127.0.0.1:8000/docs

### Start the frontend

From the frontend directory:

       npm run dev

Open the local Vite URL displayed in the terminal.

### Start the digital twin

Once both services are running, start the simulation from the DigitalTwin.ai
dashboard.

The frontend communicates with the FastAPI backend and displays the live
factory state, station intelligence, risk information, recommendations, and
what-if results.

## Demonstration scenario

The primary demonstration scenario uses Station S14.

S14 is configured to experience a controlled degradation during simulation.

The resulting operational chain is:

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
       Recommendation
              ↓
       What-if simulation
              ↓
       Downstream impact
              ↓
       Operator decision

The scenario demonstrates how a local station problem can propagate through
the production line and become an operational bottleneck.

## What-if simulation

The what-if functionality allows an operator to evaluate an intervention
without directly changing the simulated production state.

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
       Operator Decision

A what-if request can be sent to:

       POST /api/twin/what-if

Example request:

       {
       "station_id": "S14",
       "speed_change_percent": -3
       }

The response contains the baseline state, simulated state, risk change,
verdict, and estimated downstream impact.

The simulation is designed to answer:

"If we make this operational change, what is likely to happen to the
station and the downstream production line?"

## API

The backend exposes the following primary Digital Twin endpoints:

       Method	Endpoint	                    Purpose
       GET	/api/twin/state	              Overall digital twin state
       GET	/api/twin/metrics	       Factory-level KPIs
       GET	/api/twin/stations	       Station telemetry and intelligence
       GET	/api/twin/vehicles	       Vehicle and defect information
       GET	/api/twin/buffers	       Buffer state
       GET	/api/twin/graph	              Production process graph
       POST	/api/twin/start	              Start the simulation
       POST	/api/twin/stop	              Stop the simulation
       POST	/api/twin/what-if	       Run an intervention simulation

Interactive API documentation is available through FastAPI:

Open the local API documentation

### Machine learning

DigitalTwin.ai uses machine learning as one part of a broader operational
decision pipeline.

### Anomaly detection

The anomaly component evaluates station telemetry to identify abnormal
operating conditions.

### Bottleneck prediction

The bottleneck model estimates the probability that a station is becoming an
operational constraint on the production line.

### Defect-risk prediction

The defect model estimates the probability of quality-related risk for
vehicles based on available production features.

### Live inference

The live prediction layer receives the current station state and produces
updated predictions during simulation.

### Risk scoring

Anomaly and bottleneck signals are combined into a station-level operational
risk score.

### Root-cause analysis

The root-cause layer ranks contributing signals using normalized evidence from
the station state.

### Recommendations

The recommendation layer maps detected contributing signals to operational
actions and assigns priorities and confidence values.

### Testing

The backend contains test and validation scripts for major components of the
system.

Examples include:

       Factory tests
       Station tests
       Vehicle tests
       Telemetry tests
       Event processor tests
       Propagation tests
       Quality tests
       Metrics tests
       Digital twin tests
       Process graph tests
       Anomaly validation
       Bottleneck validation
       Defect validation

Representative test files include:

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

Model preparation and validation scripts are also included:

       generate_dataset.py
       create_features.py
       create_bottleneck_dataset.py
       create_defect_dataset.py
       train_anomaly.py
       train_bottleneck.py
       train_defect.py

## Troubleshooting
### Backend connection error

If the frontend reports that it cannot connect to the Digital Twin backend,
check the following:

1. Confirm that the backend virtual environment is activated.
2. Confirm that FastAPI is running.
3. Confirm that the backend is available at
       http://127.0.0.1:8000.
4. Check that VITE_API_URL points to the correct backend URL.
5. Refresh the frontend after restarting the backend.
### Frontend does not start

Run:

       npm install
       npm run dev

If dependencies are corrupted, remove node_modules and reinstall:

       Remove-Item -Recurse -Force node_modules
       npm install
       npm run dev

### ML model files are missing

The generated machine-learning artifacts are intentionally excluded from
version control.

If the required model files are not available locally, regenerate the
datasets and train the models using the scripts provided in the backend:

       generate_dataset.py
       train_anomaly.py
       train_bottleneck.py
       train_defect.py

Follow the individual scripts and their dependencies before running the live
Digital Twin.

### What-if simulation returns an error

Confirm that:

The backend is running.
The station ID exists.
The request body is valid JSON.
station_id corresponds to a valid station such as S14.
The frontend is using the correct backend API URL.
## FAQ
### What is a digital twin in this project?

DigitalTwin.ai maintains a software representation of a simulated manufacturing
environment. The representation contains stations, vehicles, buffers,
telemetry, operational state, predictions, risks, and downstream effects.

### Is this connected to a physical factory?

The current implementation is a simulation-based prototype. It demonstrates
the architecture and decision workflow using simulated manufacturing
telemetry rather than a live industrial control system.

### Why is S14 used in the demonstration?

S14 is the controlled degradation scenario used to demonstrate the complete
decision workflow from detection through what-if simulation.

### Does the system only detect anomalies?

No. The intended workflow extends beyond detection:

       Detection
       ↓
       Root Cause
       ↓
       Recommendation
       ↓
       Simulation
       ↓
       Decision

### Can recommendations be tested before applying them?

Yes. The what-if simulation evaluates an intervention against the digital twin
and estimates its effect on station risk and downstream stations.

## Project status

DigitalTwin.ai is a prototype developed for the
Accenture Innovation Challenge 2026.

The current implementation demonstrates an end-to-end manufacturing digital
twin workflow covering:

       Factory simulation
       Live telemetry
       Machine learning inference
       Anomaly detection
       Bottleneck prediction
       Defect-risk prediction
       Operational risk scoring
       Root-cause analysis
       Recommendation generation
       What-if simulation
       Downstream impact analysis
       Interactive decision support

## Maintainers
Aniket Kumar — Project developer
Accenture Innovation Challenge 2026 — Competition context