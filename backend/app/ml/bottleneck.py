import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


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
    "health",
    "health_delta",
]


class BottleneckPredictor:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight="balanced",
        )

    def fit(
        self,
        df: pd.DataFrame,
    ) -> None:

        X = df[FEATURE_COLUMNS]

        y = df["future_bottleneck"]

        self.model.fit(
            X,
            y,
        )

    def predict(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        X = df[FEATURE_COLUMNS]

        probabilities = self.model.predict_proba(X)

        result = df.copy()

        result["bottleneck_probability"] = probabilities[:, 1]

        result["bottleneck_prediction"] = result["bottleneck_probability"] >= 0.5

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
