from dataclasses import dataclass

from app.simulation.propagation import (
    calculate_downstream_impact,
)


@dataclass
class WhatIfScenario:

    station_id: str

    speed_change_percent: float = 0.0

    queue_change: int = 0

    temperature_change: float = 0.0

    vibration_change: float = 0.0

    torque_change: float = 0.0


@dataclass
class WhatIfResult:

    station_id: str

    baseline_cycle_time: float
    simulated_cycle_time: float

    baseline_queue: int
    simulated_queue: int

    baseline_temperature: float
    simulated_temperature: float

    baseline_vibration: float
    simulated_vibration: float

    baseline_torque: float
    simulated_torque: float

    baseline_risk: float
    simulated_risk: float

    downstream_impact: list[dict]


def simulate_station(
    factory,
    station,
    scenario: WhatIfScenario,
) -> WhatIfResult:

    baseline_cycle = station.cycle_time
    baseline_queue = station.queue_length
    baseline_temperature = station.temperature
    baseline_vibration = station.vibration
    baseline_torque = station.torque
    baseline_risk = station.risk_score

    # -------------------------------------
    # Speed change
    # -------------------------------------

    speed_factor = 1.0 + scenario.speed_change_percent / 100.0

    if speed_factor <= 0:
        raise ValueError("speed_change_percent must be less than 100%")

    simulated_cycle = baseline_cycle / speed_factor

    speed_reduction = max(
        0.0,
        -scenario.speed_change_percent,
    )

    # -------------------------------------
    # Physical effects
    # -------------------------------------

    simulated_vibration = (
        baseline_vibration - 0.01 * speed_reduction + scenario.vibration_change
    )

    simulated_temperature = (
        baseline_temperature - 0.30 * speed_reduction + scenario.temperature_change
    )

    simulated_torque = baseline_torque + scenario.torque_change

    # -------------------------------------
    # Queue effect
    # -------------------------------------

    simulated_queue = max(
        0,
        int(baseline_queue + scenario.queue_change),
    )

    # -------------------------------------
    # Estimate risk
    # -------------------------------------

    cycle_ratio = simulated_cycle / station.takt_time

    cycle_risk = max(
        0.0,
        min(
            1.0,
            (cycle_ratio - 0.95) / 0.25,
        ),
    )

    queue_risk = max(
        0.0,
        min(
            1.0,
            simulated_queue / 15.0,
        ),
    )

    vibration_risk = max(
        0.0,
        min(
            1.0,
            (simulated_vibration - 0.30) / 0.50,
        ),
    )

    temperature_risk = max(
        0.0,
        min(
            1.0,
            (simulated_temperature - 60.0) / 15.0,
        ),
    )

    simulated_risk = (
        0.40 * cycle_risk
        + 0.25 * queue_risk
        + 0.20 * vibration_risk
        + 0.15 * temperature_risk
    )

    simulated_risk = max(
        0.0,
        min(
            1.0,
            simulated_risk,
        ),
    )

    # -------------------------------------
    # Downstream impact
    # -------------------------------------

    cycle_time_change = simulated_cycle - baseline_cycle

    downstream_impact = calculate_downstream_impact(
        factory=factory,
        station_id=station.station_id,
        cycle_time_change=cycle_time_change,
    )

    return WhatIfResult(
        station_id=station.station_id,
        baseline_cycle_time=baseline_cycle,
        simulated_cycle_time=simulated_cycle,
        baseline_queue=baseline_queue,
        simulated_queue=simulated_queue,
        baseline_temperature=baseline_temperature,
        simulated_temperature=simulated_temperature,
        baseline_vibration=baseline_vibration,
        simulated_vibration=simulated_vibration,
        baseline_torque=baseline_torque,
        simulated_torque=simulated_torque,
        baseline_risk=baseline_risk,
        simulated_risk=simulated_risk,
        downstream_impact=downstream_impact,
    )


def scenario_verdict(
    result: WhatIfResult,
) -> str:

    risk_change = result.simulated_risk - result.baseline_risk

    if risk_change <= -0.10:
        return "strongly_recommended"

    if risk_change <= -0.03:
        return "recommended"

    if risk_change >= 0.10:
        return "not_recommended"

    if risk_change >= 0.03:
        return "high_risk"

    return "neutral"
