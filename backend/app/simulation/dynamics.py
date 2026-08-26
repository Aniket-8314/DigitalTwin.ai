import random

from app.twin.factory import Factory


def update_station(
    station,
    drift: bool = False,
) -> None:

    if drift:
        # Equipment degradation causes
        # cycle time to gradually increase.
        station.cycle_time += random.uniform(0.5, 1.2)

        # Torque starts drifting downward.
        station.torque -= random.uniform(0.1, 0.3)

        # Mechanical vibration gradually increases.
        station.vibration += random.uniform(0.01, 0.04)

        # Temperature increases slightly.
        station.temperature += random.uniform(0.1, 0.4)

        # More vehicles begin waiting.
        station.queue_length += random.choice([0, 1])

    else:
        # Normal production has small natural variation.
        station.cycle_time += random.uniform(-0.5, 0.5)

        station.temperature += random.uniform(-0.2, 0.2)

        station.vibration += random.uniform(-0.01, 0.01)

        station.torque += random.uniform(-0.1, 0.1)

        # Queue naturally fluctuates.
        station.queue_length += random.choice([-1, 0, 0, 1])

    # Keep values within reasonable ranges.
    station.cycle_time = max(
        70.0,
        min(station.cycle_time, 110.0),
    )

    station.temperature = max(
        40.0,
        min(station.temperature, 100.0),
    )

    station.vibration = max(
        0.0,
        min(station.vibration, 2.0),
    )

    station.torque = max(
        30.0,
        min(station.torque, 45.0),
    )

    station.queue_length = max(
        0,
        min(station.queue_length, 30),
    )

    station.update_health()


def update_factory(
    factory: Factory,
    drift_station: str | None = None,
) -> None:

    for station in factory.stations:

        should_drift = station.station_id == drift_station

        update_station(
            station,
            drift=should_drift,
        )
