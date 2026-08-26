import random
from datetime import datetime

from app.twin.factory import Factory
from app.twin.station import Station
from app.twin.vehicle import Vehicle
from app.twin.buffer import Buffer

from app.simulation.telemetry import Telemetry


STATION_TYPES = [
    "Body Construction",
    "Paint",
    "Powertrain",
    "Final Assembly",
]


def create_factory() -> Factory:
    factory = Factory()

    for number in range(1, 31):
        station_id = f"S{number:02d}"

        if number <= 10:
            station_type = STATION_TYPES[0]
        elif number <= 15:
            station_type = STATION_TYPES[1]
        elif number <= 20:
            station_type = STATION_TYPES[2]
        else:
            station_type = STATION_TYPES[3]

        takt_time = random.uniform(82, 88)
        cycle_time = random.uniform(78, 84)

        station = Station(
            station_id=station_id,
            name=f"{station_type} Station {number}",
            station_type=station_type,
            cycle_time=cycle_time,
            takt_time=takt_time,
            temperature=random.uniform(55, 70),
            vibration=random.uniform(0.1, 0.4),
            torque=random.uniform(38, 42),
            queue_length=random.randint(0, 4),
            sensor_available=random.random() > 0.2,
        )

        station.update_health()

        factory.add_station(station)
    buffer_positions = [5, 10, 15, 20, 25]

    for position in buffer_positions:
        buffer = Buffer(
            buffer_id=f"B{position:02d}",
            capacity=20,
            current_level=random.randint(0, 5),
        )

        factory.add_buffer(buffer)

    return factory


def create_vehicles(count: int = 20) -> list[Vehicle]:
    vehicles = []

    for number in range(1, count + 1):
        vehicle = Vehicle(vehicle_id=f"V{number:04d}")

        vehicles.append(vehicle)

    return vehicles


def generate_telemetry(
    factory: Factory,
    vehicle: Vehicle,
) -> list[Telemetry]:

    telemetry = []

    timestamp = datetime.now()

    for station in factory.stations:

        record = Telemetry(
            timestamp=timestamp,
            station_id=station.station_id,
            vehicle_id=vehicle.vehicle_id,
            cycle_time=station.cycle_time,
            temperature=station.temperature,
            vibration=station.vibration,
            torque=station.torque,
            queue_length=station.queue_length,
            sensor_available=station.sensor_available,
        )

        telemetry.append(record)

    return telemetry
