from dataclasses import dataclass

from app.twin.factory import Factory


@dataclass
class TwinMetrics:
    throughput_per_hour: float
    average_cycle_time: float
    takt_adherence: float
    average_health: float
    average_queue: float
    bottleneck_count: int
    line_health: float


def calculate_metrics(
    factory: Factory,
) -> TwinMetrics:

    stations = factory.stations

    if not stations:
        return TwinMetrics(
            throughput_per_hour=0.0,
            average_cycle_time=0.0,
            takt_adherence=0.0,
            average_health=0.0,
            average_queue=0.0,
            bottleneck_count=0,
            line_health=0.0,
        )

    # ----------------------------------------
    # Average cycle time
    # ----------------------------------------

    average_cycle_time = sum(station.cycle_time for station in stations) / len(stations)

    # ----------------------------------------
    # Average takt time
    # ----------------------------------------

    average_takt_time = sum(station.takt_time for station in stations) / len(stations)

    # ----------------------------------------
    # Takt adherence
    # ----------------------------------------

    stations_within_takt = sum(
        station.cycle_time <= station.takt_time for station in stations
    )

    takt_adherence = stations_within_takt / len(stations)

    # ----------------------------------------
    # Average health
    # ----------------------------------------

    average_health = sum(station.health for station in stations) / len(stations)

    # ----------------------------------------
    # Average queue
    # ----------------------------------------

    average_queue = sum(station.queue_length for station in stations) / len(stations)

    # ----------------------------------------
    # Bottlenecks
    # ----------------------------------------

    bottlenecks = [station for station in stations if station.is_bottleneck()]

    # ----------------------------------------
    # Approximate throughput
    #
    # The slowest effective station determines
    # the line's approximate capacity.
    # ----------------------------------------

    effective_cycle_time = max(station.cycle_time for station in stations)

    throughput_per_hour = 3600 / effective_cycle_time

    # ----------------------------------------
    # Overall line health
    # ----------------------------------------

    line_health = average_health * takt_adherence

    return TwinMetrics(
        throughput_per_hour=round(
            throughput_per_hour,
            2,
        ),
        average_cycle_time=round(
            average_cycle_time,
            2,
        ),
        takt_adherence=round(
            takt_adherence,
            4,
        ),
        average_health=round(
            average_health,
            4,
        ),
        average_queue=round(
            average_queue,
            2,
        ),
        bottleneck_count=len(bottlenecks),
        line_health=round(
            line_health,
            4,
        ),
    )
