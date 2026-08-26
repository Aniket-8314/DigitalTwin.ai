from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Vehicle:
    vehicle_id: str

    current_station: str = "S01"

    entry_time: datetime = field(default_factory=datetime.now)

    quality_score: float = 1.0

    defect_risk: float = 0.0

    defect_origin: str | None = None

    completed: bool = False

    defect_probability: float = 0.0

    defect_severity: str = "low"

    def move_to(self, station_id: str) -> None:
        self.current_station = station_id

    def update_defect_risk(self, risk: float) -> None:
        self.defect_risk = max(
            0.0,
            min(1.0, risk),
        )

    def apply_quality_damage(
        self,
        amount: float,
        origin_station: str,
    ) -> None:

        self.quality_score = max(
            0.0,
            self.quality_score - amount,
        )

        self.defect_risk = max(
            self.defect_risk,
            1.0 - self.quality_score,
        )

        if self.defect_origin is None:
            self.defect_origin = origin_station

    def mark_completed(self) -> None:
        self.completed = True
