def defect_severity(
    probability: float,
) -> str:

    if probability >= 0.75:
        return "critical"

    if probability >= 0.50:
        return "high"

    if probability >= 0.25:
        return "medium"

    return "low"
