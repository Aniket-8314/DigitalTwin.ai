from app.twin.station import Station


station = Station(
    station_id="S14",
    name="Torque Assembly",
    station_type="Final Assembly",
    cycle_time=82.0,
    takt_time=85.0,
    temperature=65.0,
    vibration=0.25,
    torque=40.0,
    queue_length=2,
)

print("Station:", station.station_id)
print("Bottleneck:", station.is_bottleneck())

station.cycle_time = 92.0
station.update_health()

print("After drift:")
print("Bottleneck:", station.is_bottleneck())
print("Health:", station.health)
