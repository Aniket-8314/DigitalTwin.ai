from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque


WINDOW_SIZE = 5


@dataclass
class StationObservation:

    cycle_time: float
    temperature: float
    vibration: float
    torque: float
    queue_length: int
    health: float


class FeatureHistory:

    def __init__(
        self,
        window_size: int = WINDOW_SIZE,
    ):

        self.window_size = window_size

        self.history: dict[str, Deque[StationObservation]] = defaultdict(
            lambda: deque(maxlen=self.window_size)
        )

    def add(
        self,
        station_id: str,
        observation: StationObservation,
    ) -> None:

        self.history[station_id].append(observation)

    def get(
        self,
        station_id: str,
    ) -> list[StationObservation]:

        return list(self.history.get(station_id, []))

    def ready(
        self,
        station_id: str,
    ) -> bool:

        return len(self.history.get(station_id, [])) >= self.window_size
