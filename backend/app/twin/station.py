from dataclasses import dataclass, field


@dataclass
class Station:
    station_id: str
    name: str
    station_type: str

    cycle_time: float
    takt_time: float

    temperature: float
    vibration: float
    torque: float

    queue_length: int

    sensor_available: bool = True

    health: float = 1.0

    anomaly_score: float = 0.0

    anomaly_severity: str = "normal"

    bottleneck_probability: float = 0.0

    risk_score: float = 0.0

    risk_severity: str = "low"

    torque_deviation: float = 0.0

    vibration_delta: float = 0.0

    cycle_time_delta: float = 0.0

    queue_delta: float = 0.0

    root_causes: list = field(default_factory=list)

    recommendations: list = field(default_factory=list)

    def is_bottleneck(self) -> bool:
        return self.cycle_time > self.takt_time

    def update_health(self) -> None:
        cycle_ratio = self.cycle_time / self.takt_time

        if cycle_ratio <= 1.0:
            self.health = 1.0
        else:
            self.health = max(
                0.0,
                1.0 - (cycle_ratio - 1.0),
            )
