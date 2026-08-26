from app.simulation.generator import create_factory, create_vehicles


factory = create_factory()
vehicles = create_vehicles(20)

for vehicle in vehicles:
    factory.add_vehicle(vehicle)


print("DIGITALTWIN.AI FACTORY")
print("----------------------")

print("Stations:", factory.station_count)
print("Vehicles:", factory.vehicle_count)

print("Buffers:", factory.buffer_count)

print("\nBuffers:")

for buffer in factory.buffers:
    print(
        buffer.buffer_id,
        "|",
        f"Level: {buffer.current_level}",
        "|",
        f"Capacity: {buffer.capacity}",
        "|",
        f"Utilization: {buffer.utilization * 100:.1f}%",
    )

print("\nStations:")

for station in factory.stations:
    print(
        station.station_id,
        "|",
        station.station_type,
        "|",
        f"Cycle: {station.cycle_time:.1f}s",
        "|",
        f"Takt: {station.takt_time:.1f}s",
        "|",
        "Sensors:",
        "YES" if station.sensor_available else "NO",
    )
