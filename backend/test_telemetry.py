from app.simulation.generator import (
    create_factory,
    create_vehicles,
    generate_telemetry,
)


factory = create_factory()

vehicles = create_vehicles(1)

vehicle = vehicles[0]

telemetry = generate_telemetry(
    factory,
    vehicle,
)


print("DIGITALTWIN.AI TELEMETRY")
print("========================")

print("Vehicle:", vehicle.vehicle_id)
print("Records:", len(telemetry))

print("\nFirst 5 records:\n")

for record in telemetry[:5]:
    print(record.to_dict())
