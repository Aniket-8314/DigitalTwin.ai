from app.simulation.generator import (
    create_factory,
    create_vehicles,
)

from app.twin.manager import DigitalTwinManager


factory = create_factory()

vehicles = create_vehicles(20)

for vehicle in vehicles:
    factory.add_vehicle(vehicle)


twin = DigitalTwinManager(factory)


print("DIGITALTWIN.AI")
print("Digital Twin State Test")
print("=" * 45)


state = twin.get_state()


print("Stations:", state.station_count)

print("Vehicles:", state.vehicle_count)

print("Buffers:", state.buffer_count)

print("\nGraph nodes:", len(state.process_graph.nodes))

print("Graph edges:", len(state.process_graph.edges))

print("S14 downstream:", state.process_graph.get_downstream("S14"))

print("\nSimulation step:", state.simulation_step)

print("Running:", state.is_running)


print("\nStarting twin...")

twin.start()

print("Running:", state.is_running)


print("\nAdvancing simulation...")

twin.advance()
twin.advance()
twin.advance()


print("Simulation step:", state.simulation_step)

print("Last updated:", state.last_updated)


print("\nStopping twin...")

twin.stop()

print("Running:", state.is_running)
