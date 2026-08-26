from app.simulation.generator import (
    create_factory,
    create_vehicles,
)

from app.simulation.quality import (
    apply_defect_scenario,
    inspect_vehicle,
)


factory = create_factory()

vehicle = create_vehicles(1)[0]


print("DIGITALTWIN.AI")
print("Quality Propagation Test")
print("=" * 45)


print("\nInitial vehicle state")

print("Quality:", f"{vehicle.quality_score * 100:.1f}%")

print("Defect risk:", f"{vehicle.defect_risk * 100:.1f}%")


# Introduce a defect at S07.

for _ in range(8):
    apply_defect_scenario(
        factory,
        vehicle,
        origin_station="S07",
    )


print("\nAfter S07 quality event")

print("Current station:", vehicle.current_station)

print("Quality:", f"{vehicle.quality_score * 100:.1f}%")

print("Defect risk:", f"{vehicle.defect_risk * 100:.1f}%")

print("Defect origin:", vehicle.defect_origin)


# Simulate vehicle reaching the quality gate.

vehicle.move_to("QUALITY_GATE")


defect_found = inspect_vehicle(
    factory,
    vehicle,
)


print("\nQuality Gate")

print("Defect detected:", defect_found)

print("Inspected:", factory.quality_gate.inspected)

print("Defects detected:", factory.quality_gate.defects_detected)

print("Defect rate:", f"{factory.quality_gate.defect_rate * 100:.1f}%")
