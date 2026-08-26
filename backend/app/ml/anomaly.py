import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "cycle_time",
    "cycle_time_mean_5",
    "cycle_time_std_5",
    "cycle_time_delta",
    "cycle_vs_takt",
    "temperature",
    "temperature_delta",
    "vibration",
    "vibration_delta",
    "torque",
    "torque_deviation",
    "queue_length",
    "queue_delta",
    "health_delta",
]


def normalize_anomaly_score(
    raw_score,
    minimum=-0.5,
    maximum=0.5,
):
    score = (maximum - raw_score) / (maximum - minimum)

    return max(
        0.0,
        min(1.0, score),
    )


def anomaly_severity(
    score: float,
) -> str:

    if score >= 0.75:
        return "critical"

    if score >= 0.50:
        return "warning"

    return "normal"


class AnomalyDetector:

    def __init__(
        self,
        contamination: float = 0.05,
    ):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42,
        )

    def fit(
        self,
        df: pd.DataFrame,
    ) -> None:

        X = df[FEATURE_COLUMNS].copy()

        self.model.fit(X)

    def predict(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        X = df[FEATURE_COLUMNS].copy()

        predictions = self.model.predict(X)

        scores = self.model.decision_function(X)

        result = df.copy()

        result["anomaly_label"] = predictions == -1

        result["anomaly_score"] = [normalize_anomaly_score(score) for score in scores]
        result["anomaly_severity"] = result["anomaly_score"].apply(anomaly_severity)

        return result

    def save(
        self,
        path: str,
    ) -> None:

        joblib.dump(
            self.model,
            path,
        )

    def load(
        self,
        path: str,
    ) -> None:

        self.model = joblib.load(path)
