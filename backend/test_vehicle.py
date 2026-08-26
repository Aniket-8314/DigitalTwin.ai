from app.twin.vehicle import Vehicle


vehicle = Vehicle(vehicle_id="V001")

print("Vehicle:", vehicle.vehicle_id)
print("Current station:", vehicle.current_station)
print("Defect risk:", vehicle.defect_risk)
print("Completed:", vehicle.completed)

vehicle.move_to("S14")
vehicle.update_defect_risk(0.72)

print("\nAfter moving to S14:")
print("Current station:", vehicle.current_station)
print("Defect risk:", vehicle.defect_risk)

vehicle.move_to("S30")
vehicle.mark_completed()

print("\nAfter completing production:")
print("Current station:", vehicle.current_station)
print("Completed:", vehicle.completed)
