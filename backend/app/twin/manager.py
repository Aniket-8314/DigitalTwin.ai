from app.twin.factory import Factory
from app.twin.graph_builder import (
    build_process_graph,
)
from app.twin.state import DigitalTwinState


class DigitalTwinManager:

    def __init__(
        self,
        factory: Factory,
    ):

        process_graph = build_process_graph(factory)

        self.state = DigitalTwinState(
            factory=factory,
            process_graph=process_graph,
        )

    def start(self) -> None:

        self.state.is_running = True

        self.state.update_timestamp()

    def stop(self) -> None:

        self.state.is_running = False

        self.state.update_timestamp()

    def advance(
        self,
        update_timestamp: bool = True,
    ) -> None:

        self.state.simulation_step += 1

        if update_timestamp:

            self.state.update_timestamp()

    def get_state(
        self,
    ) -> DigitalTwinState:

        return self.state
