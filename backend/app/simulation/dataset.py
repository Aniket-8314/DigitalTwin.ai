import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from app.simulation.dynamics import update_factory
from app.simulation.generator import (
    create_factory,
    create_vehicles,
)
from app.simulation.quality import (
    apply_defect_scenario,
)
from app.simulation.propagation import (
    propagate_line_effects,
)


OUTPUT_PATH = Path("data/production_events.csv")


FIELDS = [
    "timestamp",
    "vehicle_id",
    "station_id",
    "cycle_time",
    "takt_time",
    "temperature",
    "vibration",
    "torque",
    "queue_length",
    "sensor_available",
    "health",
    "quality_score",
    "defect_risk",
    "defect_origin",
]


def generate_dataset(
    vehicles_count: int = 50,
    steps: int = 100,
) -> None:

    factory = create_factory()

    vehicles = create_vehicles(vehicles_count)

    rows = []

    start_time = datetime.now()

    for step in range(steps):

        timestamp = start_time + timedelta(seconds=step * 30)

        # ----------------------------------
        # Production scenarios
        # ----------------------------------

        if 20 <= step < 55:

            # Equipment degradation at S14
            update_factory(
                factory,
                drift_station="S14",
            )

        else:

            update_factory(factory)

        # ----------------------------------
        # Line propagation
        # ----------------------------------

        propagate_line_effects(factory)

        # ----------------------------------
        # Generate vehicle observations
        # ----------------------------------

        for vehicle in vehicles:

            # Randomly assign vehicles
            # to stations for this dataset.
            station = random.choice(factory.stations)

            vehicle.move_to(station.station_id)

            # --------------------------------
            # Quality event
            # --------------------------------

            if 30 <= step < 70 and station.station_id == "S07":

                apply_defect_scenario(
                    factory,
                    vehicle,
                    origin_station="S07",
                )

            # --------------------------------
            # Create dataset rows
            # --------------------------------

            rows.append(
                {
                    "timestamp": timestamp.isoformat(),
                    "vehicle_id": vehicle.vehicle_id,
                    "station_id": station.station_id,
                    "cycle_time": round(
                        station.cycle_time,
                        3,
                    ),
                    "takt_time": round(
                        station.takt_time,
                        3,
                    ),
                    "temperature": round(
                        station.temperature,
                        3,
                    ),
                    "vibration": round(
                        station.vibration,
                        3,
                    ),
                    "torque": round(
                        station.torque,
                        3,
                    ),
                    "queue_length": station.queue_length,
                    "sensor_available": station.sensor_available,
                    "health": round(
                        station.health,
                        4,
                    ),
                    "quality_score": round(
                        vehicle.quality_score,
                        4,
                    ),
                    "defect_risk": round(
                        vehicle.defect_risk,
                        4,
                    ),
                    "defect_origin": vehicle.defect_origin or "",
                }
            )

    # --------------------------------------
    # Write CSV
    # --------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )

        writer.writeheader()

        writer.writerows(rows)

    print(f"Dataset generated: {OUTPUT_PATH}")

    print(f"Total records: {len(rows)}")
