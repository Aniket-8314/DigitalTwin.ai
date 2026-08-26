def calculate_station_risk(
    anomaly_score: float,
    bottleneck_probability: float,
) -> float:

    risk = 0.45 * anomaly_score + 0.55 * bottleneck_probability

    return round(
        max(0.0, min(1.0, risk)),
        4,
    )


def risk_severity(
    risk: float,
) -> str:

    if risk >= 0.75:
        return "critical"

    if risk >= 0.50:
        return "high"

    if risk >= 0.25:
        return "medium"

    return "low"
