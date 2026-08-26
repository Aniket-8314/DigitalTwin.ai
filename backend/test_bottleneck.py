from app.simulation.dynamics import update_factory
from app.simulation.generator import create_factory


factory = create_factory()


for step in range(20):

    update_factory(
        factory,
        drift_station="S14",
    )

    bottlenecks = factory.bottleneck_stations

    print(f"Step {step + 1}: " f"{len(bottlenecks)} bottleneck(s)")

    for station in bottlenecks:
        print(
            f"  {station.station_id} "
            f"→ cycle={station.cycle_time:.1f}s "
            f"takt={station.takt_time:.1f}s"
        )
