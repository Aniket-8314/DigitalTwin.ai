from app.simulation.generator import (
    create_factory,
    create_vehicles,
)

from app.simulation.stream import generate_stream


factory = create_factory()

vehicle = create_vehicles(1)[0]


print("DIGITALTWIN.AI")
print("Scenario: S14 Torque Drift")
print("=" * 40)


for step, telemetry in enumerate(
    generate_stream(
        factory,
        vehicle,
        steps=20,
        delay=0.5,
        drift_station="S14",
    ),
    start=1,
):

    station = telemetry[13]

    print(f"\nStep {step}")

    print(
        "Station:",
        station.station_id,
    )

    print(
        "Cycle Time:",
        f"{station.cycle_time:.2f}s",
    )

    print(
        "Torque:",
        f"{station.torque:.2f}",
    )

    print(
        "Vibration:",
        f"{station.vibration:.2f}",
    )

    print(
        "Temperature:",
        f"{station.temperature:.2f}°C",
    )

    print(
        "Queue:",
        station.queue_length,
    )

    actual_station = factory.get_station("S14")
    print(
        "Health:",
        f"{actual_station.health * 100:.1f}%",
    )
