from dataclasses import dataclass, field
from datetime import datetime

from app.twin.factory import Factory
from app.twin.graph import ProcessGraph
from app.twin.metrics import TwinMetrics, calculate_metrics


@dataclass
class DigitalTwinState:

    factory: Factory

    process_graph: ProcessGraph

    last_updated: datetime = field(default_factory=datetime.now)

    simulation_step: int = 0

    is_running: bool = False

    def update_timestamp(self) -> None:

        self.last_updated = datetime.now()

    def advance_step(self) -> None:

        self.simulation_step += 1

        self.update_timestamp()

    @property
    def station_count(self) -> int:

        return self.factory.station_count

    @property
    def vehicle_count(self) -> int:

        return self.factory.vehicle_count

    @property
    def buffer_count(self) -> int:

        return self.factory.buffer_count

    @property
    def metrics(self) -> TwinMetrics:

        return calculate_metrics(self.factory)
