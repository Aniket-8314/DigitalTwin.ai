from dataclasses import dataclass


@dataclass
class RootCause:

    signal: str

    score: float

    direction: str

    evidence: str


def _normalize(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if maximum <= minimum:
        return 0.0

    score = (value - minimum) / (maximum - minimum)

    return max(
        0.0,
        min(1.0, score),
    )


def rank_root_causes(
    station,
) -> list[RootCause]:

    causes = []

    # ----------------------------------------
    # 1. Torque deviation
    # ----------------------------------------

    torque_deviation = abs(
        getattr(
            station,
            "torque_deviation",
            0.0,
        )
    )

    torque_score = _normalize(
        torque_deviation,
        0.0,
        5.0,
    )

    if torque_score > 0:

        causes.append(
            RootCause(
                signal="Torque deviation",
                score=torque_score,
                direction="down",
                evidence=(f"Torque deviation " f"{torque_deviation:.2f}"),
            )
        )

    # ----------------------------------------
    # 2. Vibration
    # ----------------------------------------

    vibration = station.vibration

    vibration_trend = getattr(
        station,
        "vibration_delta",
        0.0,
    )

    vibration_score = 0.7 * _normalize(
        vibration,
        0.30,
        0.80,
    ) + 0.3 * _normalize(
        vibration_trend,
        0.0,
        0.10,
    )

    if vibration_score > 0:

        causes.append(
            RootCause(
                signal="Vibration increase",
                score=vibration_score,
                direction="up",
                evidence=(f"Vibration " f"{vibration:.2f}"),
            )
        )

    # ----------------------------------------
    # 3. Cycle time
    # ----------------------------------------

    cycle_ratio = station.cycle_time / station.takt_time

    cycle_trend = getattr(
        station,
        "cycle_time_delta",
        0.0,
    )

    cycle_score = 0.7 * _normalize(
        cycle_ratio,
        0.95,
        1.20,
    ) + 0.3 * _normalize(
        cycle_trend,
        0.0,
        3.0,
    )

    if cycle_score > 0:

        causes.append(
            RootCause(
                signal="Cycle-time deviation",
                score=cycle_score,
                direction="up",
                evidence=(f"Cycle/takt ratio " f"{cycle_ratio:.2f}"),
            )
        )

    # ----------------------------------------
    # 4. Queue growth
    # ----------------------------------------

    queue = station.queue_length

    queue_score = _normalize(
        queue,
        2.0,
        15.0,
    )

    if queue_score > 0:

        causes.append(
            RootCause(
                signal="Queue buildup",
                score=queue_score,
                direction="up",
                evidence=(f"Queue length " f"{queue}"),
            )
        )

    # ----------------------------------------
    # 5. Temperature
    # ----------------------------------------

    temperature = station.temperature

    temperature_score = _normalize(
        temperature,
        65.0,
        75.0,
    )

    if temperature_score > 0:

        causes.append(
            RootCause(
                signal="Temperature increase",
                score=temperature_score,
                direction="up",
                evidence=(f"Temperature " f"{temperature:.1f}°C"),
            )
        )

    # ----------------------------------------
    # Sort strongest signals first
    # ----------------------------------------

    causes.sort(
        key=lambda cause: cause.score,
        reverse=True,
    )

    return causes
