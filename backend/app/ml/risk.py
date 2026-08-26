from dataclasses import dataclass


@dataclass
class StationRisk:

    station_id: str

    anomaly_score: float = 0.0

    anomaly_severity: str = "normal"

    bottleneck_probability: float = 0.0

    defect_probability: float = 0.0

    confidence: float = 0.0