import time

from app.simulation.dynamics import update_factory
from app.simulation.generator import generate_telemetry
from app.simulation.propagation import propagate_line_effects
from app.twin.factory import Factory
from app.twin.vehicle import Vehicle


def generate_stream(
    factory: Factory,
    vehicle: Vehicle,
    steps: int = 10,
    delay: float = 0.5,
    drift_station: str | None = None,
):

    for step in range(steps):

        # Update physical factory state.
        update_factory(
            factory,
            drift_station=drift_station,
        )

        propagate_line_effects(factory)

        # Read the updated physical state.
        telemetry = generate_telemetry(
            factory,
            vehicle,
        )

        yield telemetry

        time.sleep(delay)
