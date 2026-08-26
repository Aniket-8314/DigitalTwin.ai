import pandas as pd

from app.ml.anomaly import (
    AnomalyDetector,
)


DATA_FILE = "data/features.csv"

MODEL_FILE = "data/anomaly_model.joblib"


df = pd.read_csv(DATA_FILE)


detector = AnomalyDetector()

detector.load(MODEL_FILE)


result = detector.predict(df)


print("DIGITALTWIN.AI")

print("Anomaly Detection")

print("=" * 50)


print(
    "Total records:",
    len(result),
)


print(
    "Anomalies:",
    result["anomaly_label"].sum(),
)


print("Anomaly rate:", f"{result['anomaly_label'].mean() * 100:.2f}%")


print("\nTop anomalies:")


columns = [
    "timestamp",
    "station_id",
    "cycle_time",
    "vibration",
    "torque",
    "queue_length",
    "anomaly_score",
    "anomaly_severity",
]


top = result.sort_values(
    "anomaly_score",
    ascending=False,
).head(10)


print(top[columns].to_string(index=False))
