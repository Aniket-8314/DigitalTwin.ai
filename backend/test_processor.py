from datetime import datetime

from app.simulation.generator import (
    create_factory,
    create_vehicles,
)

from app.twin.event import TelemetryEvent
from app.twin.manager import DigitalTwinManager
from app.twin.processor import EventProcessor


# -----------------------------------------
# Create factory
# -----------------------------------------

factory = create_factory()

vehicles = create_vehicles(20)

for vehicle in vehicles:
    factory.add_vehicle(vehicle)


# -----------------------------------------
# Create Digital Twin
# -----------------------------------------

twin = DigitalTwinManager(factory)

processor = EventProcessor(twin)


# -----------------------------------------
# Check original station state
# -----------------------------------------

station = factory.get_station("S14")

print("BEFORE EVENT")
print("=" * 40)

print("Station:", station.station_id)

print("Cycle:", station.cycle_time)

print("Torque:", station.torque)

print("Vibration:", station.vibration)


# -----------------------------------------
# Create incoming telemetry
# -----------------------------------------

event = TelemetryEvent(
    timestamp=datetime.now(),
    station_id="S14",
    vehicle_id="V0001",
    cycle_time=95.0,
    temperature=72.0,
    vibration=0.85,
    torque=35.5,
    queue_length=14,
    sensor_available=True,
)


# -----------------------------------------
# Process event
# -----------------------------------------

processor.process(event)


# -----------------------------------------
# Check updated state
# -----------------------------------------

print("\nAFTER EVENT")
print("=" * 40)

print("Station:", station.station_id)

print("Cycle:", station.cycle_time)

print("Torque:", station.torque)

print("Vibration:", station.vibration)

print("Queue:", station.queue_length)

print("Health:", f"{station.health * 100:.1f}%")

print("Simulation step:", twin.state.simulation_step)

print("Last updated:", twin.state.last_updated)
