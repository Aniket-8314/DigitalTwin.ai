# DigitalTwin.ai

AI-powered digital twin for predictive manufacturing operations.

DigitalTwin.ai combines real-time factory simulation, machine-learning-based anomaly detection, bottleneck prediction, defect-risk estimation, root-cause analysis, AI recommendations, and what-if simulation into a single operational decision-support system.

## ?? Core Capabilities

- Live manufacturing digital twin
- Real-time station telemetry
- Anomaly detection
- Bottleneck prediction
- Defect-risk prediction
- Station-level risk scoring
- Root-cause analysis
- Confidence-aware recommendations
- What-if intervention simulation
- Downstream impact analysis
- Interactive production-line visualization

## ??? Architecture

`	ext
Factory Simulation
       ?
Telemetry Generation
       ?
Digital Twin
       ?
 +-----+---------------+
 ?     ?               ?
Anomaly Bottleneck   Defect
 ?     ?               ?
 +-----+---------------+
       ?
   Risk Scoring
       ?
 Root Cause Analysis
       ?
 Recommendations
       ?
 What-If Simulation
       ?
 Downstream Impact
       ?
 Operator Decision
?? Project Structure
DigitalTwin.ai/
¦
+-- backend/
¦   +-- app/
¦   ¦   +-- api/
¦   ¦   +-- ml/
¦   ¦   +-- simulation/
¦   ¦   +-- twin/
¦   +-- main.py
¦   +-- requirements.txt
¦   +-- generate_dataset.py
¦   +-- train_anomaly.py
¦   +-- train_bottleneck.py
¦   +-- train_defect.py
¦   +-- test_*.py
¦
+-- frontend/
¦   +-- src/
¦   +-- public/
¦   +-- package.json
¦   +-- vite.config.js
¦
+-- README.md
?? Backend Setup
cd backend

python -m venv .venv
Windows
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the backend:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
?? Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Then open the Vite development URL shown in the terminal.

?? Demo Scenario

The primary demonstration scenario uses station S14.

S14 Torque Drift
       ?
Torque degradation
       ?
Vibration increase
       ?
Cycle-time increase
       ?
Queue buildup
       ?
Bottleneck detection
       ?
Risk escalation
       ?
Root-cause analysis
       ?
Recommendation
       ?
What-if simulation
       ?
Downstream impact
?? Decision Intelligence

The system follows a closed operational decision loop:

Observe ? Detect ? Explain ? Recommend ? Simulate ? Decide

??? Technology Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
Scikit-learn
Pandas
NumPy
Intelligence
Anomaly detection
Bottleneck prediction
Defect-risk prediction
Root-cause ranking
Risk scoring
What-if simulation
?? Project Status

Prototype completed for the Accenture Innovation Challenge 2026.

The current implementation focuses on demonstrating an end-to-end manufacturing digital-twin workflow from live simulation to decision support.

?? Team

Built for the Accenture Innovation Challenge 2026.

