from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Telemetry:
    timestamp: datetime

    station_id: str
    vehicle_id: str

    cycle_time: float
    temperature: float
    vibration: float
    torque: float

    queue_length: int

    sensor_available: bool

    def to_dict(self) -> dict:
        data = asdict(self)

        data["timestamp"] = self.timestamp.isoformat()

        return data
