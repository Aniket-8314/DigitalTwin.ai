from fastapi import APIRouter

from app.simulation.generator import (
    create_factory,
    create_vehicles,
)

from app.twin.manager import DigitalTwinManager
from app.twin.engine import TwinEngine
from app.ml.impact import (
    downstream_nodes,
)

from pydantic import BaseModel

from app.simulation.what_if import (
    WhatIfScenario,
    simulate_station,
    scenario_verdict,
)

router = APIRouter(
    prefix="/api/twin",
    tags=["Digital Twin"],
)


# ------------------------------------------------
# Create the Digital Twin
# ------------------------------------------------

factory = create_factory()

vehicles = create_vehicles(20)

for vehicle in vehicles:
    factory.add_vehicle(vehicle)


twin = DigitalTwinManager(factory)
engine = TwinEngine(
    twin,
    interval=1.0,
)


class WhatIfRequest(BaseModel):

    station_id: str

    speed_change_percent: float = 0.0

    queue_change: int = 0

    temperature_change: float = 0.0

    vibration_change: float = 0.0

    torque_change: float = 0.0


# ------------------------------------------------
# Overall Twin State
# ------------------------------------------------


@router.get("/state")
def get_twin_state():

    state = twin.get_state()

    return {
        "simulation_step": state.simulation_step,
        "last_updated": state.last_updated.isoformat(),
        "is_running": state.is_running,
        "stations": state.station_count,
        "vehicles": state.vehicle_count,
        "buffers": state.buffer_count,
    }


# ------------------------------------------------
# Station State
# ------------------------------------------------


@router.get("/stations")
def get_stations():

    stations = twin.state.factory.stations

    return [
        {
            "station_id": station.station_id,
            "name": station.name,
            "type": station.station_type,
            "cycle_time": station.cycle_time,
            "takt_time": station.takt_time,
            "temperature": station.temperature,
            "vibration": station.vibration,
            "torque": station.torque,
            "queue_length": station.queue_length,
            "sensor_available": station.sensor_available,
            "health": station.health,
            "bottleneck": station.is_bottleneck(),
            "bottleneck_probability": station.bottleneck_probability,
            "anomaly_score": station.anomaly_score,
            "anomaly_severity": station.anomaly_severity,
            "risk_score": station.risk_score,
            "risk_severity": station.risk_severity,
            "root_causes": [
                {
                    "signal": cause.signal,
                    "score": cause.score,
                    "direction": cause.direction,
                    "evidence": cause.evidence,
                }
                for cause in station.root_causes
            ],
            "downstream_impact": downstream_nodes(
                twin.state.process_graph, station.station_id
            ),
            "recommendations": [
                {
                    "action": recommendation.action,
                    "priority": recommendation.priority,
                    "reason": recommendation.reason,
                    "expected_effect": recommendation.expected_effect,
                    "confidence": recommendation.confidence,
                }
                for recommendation in station.recommendations
            ],
        }
        for station in stations
    ]


# ------------------------------------------------
# Vehicle State
# ------------------------------------------------


@router.get("/vehicles")
def get_vehicles():

    vehicles = twin.state.factory.vehicles

    return [
        {
            "vehicle_id": vehicle.vehicle_id,
            "current_station": vehicle.current_station,
            "quality_score": vehicle.quality_score,
            "defect_risk": vehicle.defect_risk,
            "defect_origin": vehicle.defect_origin,
            "defect_probability": vehicle.defect_probability,
            "defect_severity": vehicle.defect_severity,
            "completed": vehicle.completed,
        }
        for vehicle in vehicles
    ]


# ------------------------------------------------
# Buffer State
# ------------------------------------------------


@router.get("/buffers")
def get_buffers():

    buffers = twin.state.factory.buffers

    return [
        {
            "buffer_id": buffer.buffer_id,
            "current_level": buffer.current_level,
            "capacity": buffer.capacity,
            "utilization": buffer.utilization,
        }
        for buffer in buffers
    ]


# ------------------------------------------------
# Twin Metrics
# ------------------------------------------------


@router.get("/metrics")
def get_metrics():

    metrics = twin.state.metrics

    return {
        "throughput_per_hour": metrics.throughput_per_hour,
        "average_cycle_time": metrics.average_cycle_time,
        "takt_adherence": metrics.takt_adherence,
        "average_health": metrics.average_health,
        "average_queue": metrics.average_queue,
        "bottleneck_count": metrics.bottleneck_count,
        "line_health": metrics.line_health,
    }


# ------------------------------------------------
# Process Graph
# ------------------------------------------------


@router.get("/graph")
def get_graph():

    graph = twin.state.process_graph

    return {
        "nodes": [
            {
                "id": node.node_id,
                "type": node.node_type,
            }
            for node in graph.nodes.values()
        ],
        "edges": [
            {
                "source": edge.source,
                "target": edge.target,
            }
            for edge in graph.edges
        ],
    }


@router.post("/start")
def start_twin():

    engine.start()

    return {"status": "running"}


@router.post("/stop")
def stop_twin():

    engine.stop()

    return {"status": "stopped"}


@router.post("/what-if")
def what_if(
    request: WhatIfRequest,
):

    station = twin.state.factory.get_station(request.station_id)

    if station is None:

        return {"error": (f"Station " f"{request.station_id} " f"not found")}

    scenario = WhatIfScenario(
        station_id=request.station_id,
        speed_change_percent=(request.speed_change_percent),
        queue_change=(request.queue_change),
        temperature_change=(request.temperature_change),
        vibration_change=(request.vibration_change),
        torque_change=(request.torque_change),
    )

    result = simulate_station(
        factory=twin.state.factory,
        station=station,
        scenario=scenario,
    )

    verdict = scenario_verdict(result)

    return {
        "station_id": result.station_id,
        "baseline": {
            "cycle_time": result.baseline_cycle_time,
            "queue": result.baseline_queue,
            "temperature": result.baseline_temperature,
            "vibration": result.baseline_vibration,
            "torque": result.baseline_torque,
            "risk": result.baseline_risk,
        },
        "simulation": {
            "cycle_time": result.simulated_cycle_time,
            "queue": result.simulated_queue,
            "temperature": result.simulated_temperature,
            "vibration": result.simulated_vibration,
            "torque": result.simulated_torque,
            "risk": result.simulated_risk,
        },
        "risk_change": (result.simulated_risk - result.baseline_risk),
        "verdict": verdict,
        "downstream_impact": result.downstream_impact,
    }
