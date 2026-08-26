import pandas as pd

from app.ml.anomaly import (
    AnomalyDetector,
)


INPUT_FILE = "data/features.csv"

MODEL_FILE = "data/anomaly_model.joblib"


df = pd.read_csv(INPUT_FILE)


print("Training anomaly detector...")

print(
    "Training records:",
    len(df),
)


detector = AnomalyDetector(contamination=0.05)

detector.fit(df)

detector.save(MODEL_FILE)


print("Model saved:", MODEL_FILE)
