from dataclasses import dataclass


@dataclass
class Recommendation:

    action: str
    priority: str
    reason: str
    expected_effect: str
    confidence: float = 0.5


def get_cause_score(
    signal: str,
    causes,
) -> float:

    for cause in causes:

        if cause.signal == signal:
            return cause.score

    return 0.0


def generate_recommendations(
    station,
) -> list[Recommendation]:

    recommendations = []

    causes = getattr(
        station,
        "root_causes",
        [],
    )

    # -----------------------------------------
    # Torque
    # -----------------------------------------

    torque_confidence = get_cause_score(
        "Torque deviation",
        causes,
    )

    if torque_confidence > 0:

        recommendations.append(
            Recommendation(
                action=(
                    "Inspect and recalibrate "
                    f"the torque tool at "
                    f"{station.station_id}"
                ),
                priority="high",
                reason=(
                    "Torque deviation is " "one of the strongest " "risk contributors."
                ),
                expected_effect=(
                    "Reduce assembly variation " "and defect probability."
                ),
                confidence=torque_confidence,
            )
        )

    # -----------------------------------------
    # Vibration
    # -----------------------------------------

    vibration_confidence = get_cause_score(
        "Vibration increase",
        causes,
    )

    if vibration_confidence > 0:

        recommendations.append(
            Recommendation(
                action=(
                    "Inspect mechanical components "
                    "and tooling at "
                    f"{station.station_id}"
                ),
                priority="high",
                reason=(
                    "Vibration is increasing " "and contributing to " "station risk."
                ),
                expected_effect=(
                    "Reduce mechanical instability " "and prevent further degradation."
                ),
                confidence=vibration_confidence,
            )
        )

    # -----------------------------------------
    # Cycle time
    # -----------------------------------------

    cycle_confidence = get_cause_score(
        "Cycle-time deviation",
        causes,
    )

    if cycle_confidence > 0:

        recommendations.append(
            Recommendation(
                action=(
                    "Reduce operating speed by "
                    "approximately 3% while "
                    "investigating the station."
                ),
                priority="medium",
                reason=("Cycle time is exceeding " "the expected takt."),
                expected_effect=(
                    "Reduce queue growth and " "stabilize downstream flow."
                ),
                confidence=cycle_confidence,
            )
        )

    # -----------------------------------------
    # Queue
    # -----------------------------------------

    queue_confidence = get_cause_score(
        "Queue buildup",
        causes,
    )

    if queue_confidence > 0:

        recommendations.append(
            Recommendation(
                action=(
                    "Monitor downstream buffer "
                    "capacity and temporarily "
                    "rebalance workload."
                ),
                priority="medium",
                reason=("Queue buildup indicates " "flow imbalance."),
                expected_effect=(
                    "Reduce downstream congestion " "and propagation risk."
                ),
                confidence=queue_confidence,
            )
        )

    # -----------------------------------------
    # Temperature
    # -----------------------------------------

    temperature_confidence = get_cause_score(
        "Temperature increase",
        causes,
    )

    if temperature_confidence > 0:

        recommendations.append(
            Recommendation(
                action=(
                    "Inspect cooling and thermal "
                    "conditions at "
                    f"{station.station_id}"
                ),
                priority="medium",
                reason=("Temperature is above " "the normal operating range."),
                expected_effect=("Prevent thermal degradation " "and sensor drift."),
                confidence=temperature_confidence,
            )
        )

    # -----------------------------------------
    # Fallback
    # -----------------------------------------

    if not recommendations:

        recommendations.append(
            Recommendation(
                action=("Continue monitoring " f"{station.station_id}"),
                priority="low",
                reason=("No dominant contributing " "signal has been identified."),
                expected_effect=("Maintain current operating " "conditions."),
                confidence=0.30,
            )
        )

    # -----------------------------------------
    # Priority ordering
    # -----------------------------------------

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item.priority,
            99,
        )
    )

    return recommendations
