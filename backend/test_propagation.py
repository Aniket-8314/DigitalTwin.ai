from app.simulation.dynamics import update_factory
from app.simulation.generator import create_factory
from app.simulation.propagation import propagate_line_effects


factory = create_factory()

print("DIGITALTWIN.AI")
print("Line Propagation Test")
print("=" * 45)


for step in range(20):

    update_factory(
        factory,
        drift_station="S14",
    )
    propagate_line_effects(factory)

    station_14 = factory.get_station("S14")
    station_15 = factory.get_station("S15")
    station_16 = factory.get_station("S16")

    buffer_15 = factory.get_buffer("B15")

    print(f"\nStep {step + 1}")

    print(
        f"S14 → cycle: "
        f"{station_14.cycle_time:.1f}s | "
        f"queue: {station_14.queue_length}"
    )

    print(f"B15 → " f"{buffer_15.current_level}/" f"{buffer_15.capacity}")

    print(
        f"S15 → cycle: "
        f"{station_15.cycle_time:.1f}s | "
        f"queue: {station_15.queue_length}"
    )

    print(
        f"S16 → cycle: "
        f"{station_16.cycle_time:.1f}s | "
        f"queue: {station_16.queue_length}"
    )
