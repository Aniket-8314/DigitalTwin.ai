from app.twin.factory import Factory
from app.twin.vehicle import Vehicle


def apply_defect_scenario(
    factory: Factory,
    vehicle: Vehicle,
    origin_station: str = "S07",
) -> None:

    station = factory.get_station(
        origin_station
    )

    if station is None:
        return

    # -----------------------------------------
    # Calculate degradation from station state
    # -----------------------------------------

    damage = 0.10

    if station.vibration > 0.5:
        damage += 0.04

    if station.vibration > 0.7:
        damage += 0.05

    if station.torque < 38:
        damage += 0.04

    if station.torque < 36:
        damage += 0.05

    if station.cycle_time > station.takt_time:
        damage += 0.03

    # -----------------------------------------
    # Apply quality degradation
    # -----------------------------------------

    vehicle.apply_quality_damage(
        amount=damage,
        origin_station=origin_station,
    )


def inspect_vehicle(
    factory: Factory,
    vehicle: Vehicle,
) -> bool:

    return factory.quality_gate.inspect(
        vehicle
    )