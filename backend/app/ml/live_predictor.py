from app.ml.anomaly import (
    AnomalyDetector,
)

from app.ml.bottleneck import (
    BottleneckPredictor,
)

from app.ml.history import (
    FeatureHistory,
    StationObservation,
)

from app.ml.defect import (
    DefectPredictor,
)

from app.ml.live_features import (
    build_live_features,
)


class LivePredictor:

    def __init__(
        self,
        anomaly_model_path: str,
        bottleneck_model_path: str,
        defect_model_path: str,
    ):

        self.anomaly = AnomalyDetector()

        self.anomaly.load(anomaly_model_path)

        self.bottleneck = BottleneckPredictor()

        self.bottleneck.load(bottleneck_model_path)

        self.history = FeatureHistory()
        self.defect = DefectPredictor()

        self.defect.load(defect_model_path)

    def update(
        self,
        station,
    ) -> dict | None:

        observation = StationObservation(
            cycle_time=station.cycle_time,
            temperature=station.temperature,
            vibration=station.vibration,
            torque=station.torque,
            queue_length=station.queue_length,
            health=station.health,
        )

        self.history.add(
            station.station_id,
            observation,
        )

        if not self.history.ready(station.station_id):
            return None

        features = build_live_features(
            history=self.history,
            station_id=station.station_id,
            takt_time=station.takt_time,
            sensor_available=(station.sensor_available),
        )

        if features.empty:
            return None

        current = features.tail(1)

        anomaly_result = self.anomaly.predict(current)

        bottleneck_result = self.bottleneck.predict(current)

        defect_result = self.defect.predict(current)

        defect_probability = float(defect_result["defect_probability"].iloc[0])

        anomaly_score = float(anomaly_result["anomaly_score"].iloc[0])

        anomaly_severity = anomaly_result["anomaly_severity"].iloc[0]

        bottleneck_probability = float(
            bottleneck_result["bottleneck_probability"].iloc[0]
        )

        return {
            "anomaly_score": anomaly_score,
            "anomaly_severity": anomaly_severity,
            "bottleneck_probability": bottleneck_probability,
            "defect_probability": defect_probability,
        }
