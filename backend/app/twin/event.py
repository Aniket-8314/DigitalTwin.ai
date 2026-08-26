from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelemetryEvent:
    timestamp: datetime

    station_id: str
    vehicle_id: str

    cycle_time: float
    temperature: float
    vibration: float
    torque: float

    queue_length: int

    sensor_available: bool