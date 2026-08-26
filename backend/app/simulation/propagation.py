from app.twin.factory import Factory


def propagate_line_effects(factory: Factory) -> None:
    """
    Propagate station conditions through downstream buffers
    and stations.
    """

    # -----------------------------------------
    # 1. Move excess queue into downstream buffer
    # -----------------------------------------

    for position in [5, 10, 15, 20, 25]:

        station = factory.get_station(f"S{position:02d}")

        buffer = factory.get_buffer(f"B{position:02d}")

        if station is None or buffer is None:
            continue

        # If station queue is high,
        # upstream pressure enters the buffer.
        if station.queue_length > 5:

            excess = station.queue_length - 5

            buffer.add(excess)

            station.queue_length = 5

    # -----------------------------------------
    # 2. Buffer pressure affects next section
    # -----------------------------------------

    for position in [5, 10, 15, 20, 25]:

        buffer = factory.get_buffer(f"B{position:02d}")

        if buffer is None:
            continue

        next_station_number = position + 1

        if next_station_number > 30:
            continue

        next_station = factory.get_station(f"S{next_station_number:02d}")

        if next_station is None:
            continue

        utilization = buffer.utilization

        # High buffer utilization creates
        # downstream pressure.
        if utilization > 0.7:

            pressure = (utilization - 0.7) * 10

            next_station.cycle_time += pressure

            next_station.queue_length += 1

            next_station.update_health()


def calculate_downstream_impact(
    factory: Factory,
    station_id: str,
    cycle_time_change: float,
) -> list[dict]:
    """
    Calculate estimated downstream impact without
    modifying the live factory.
    """

    station = factory.get_station(station_id)

    if station is None:
        return []

    impacts = []

    current_cycle_change = cycle_time_change

    current_position = int(station_id[1:])

    for depth in range(1, 5):

        next_position = current_position + depth

        if next_position > 30:
            break

        downstream = factory.get_station(f"S{next_position:02d}")

        if downstream is None:
            continue

        # -------------------------------------
        # Propagation attenuation
        # -------------------------------------

        propagated_change = current_cycle_change * (0.65**depth)

        simulated_cycle = downstream.cycle_time + propagated_change

        queue_impact = max(
            0,
            int(propagated_change / 2),
        )

        simulated_queue = downstream.queue_length + queue_impact

        health_penalty = propagated_change * 0.01

        simulated_health = max(
            0.0,
            downstream.health - health_penalty,
        )

        impacts.append(
            {
                "station_id": downstream.station_id,
                "baseline_cycle_time": downstream.cycle_time,
                "simulated_cycle_time": simulated_cycle,
                "baseline_queue": downstream.queue_length,
                "simulated_queue": simulated_queue,
                "baseline_health": downstream.health,
                "simulated_health": simulated_health,
            }
        )

    return impacts


def simulate_downstream_effects(
    factory: Factory,
    station_id: str,
    steps: int = 3,
) -> list[dict]:
    """
    Estimate how a station intervention propagates
    through downstream stations.

    This function is intended for what-if simulation
    and does not replace the live propagation logic.
    """

    station = factory.get_station(station_id)

    if station is None:
        return []

    results = []

    current_position = int(station_id[1:])

    for step in range(1, steps + 1):

        next_position = current_position + step

        if next_position > 30:
            break

        downstream = factory.get_station(f"S{next_position:02d}")

        if downstream is None:
            continue

        results.append(
            {
                "station_id": downstream.station_id,
                "cycle_time": downstream.cycle_time,
                "queue_length": downstream.queue_length,
                "health": downstream.health,
            }
        )

    return results
