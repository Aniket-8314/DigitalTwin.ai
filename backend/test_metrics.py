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


metrics = twin.state.metrics


print("DIGITALTWIN.AI")
print("Twin Metrics")
print("=" * 45)

print(
    "Throughput:",
    f"{metrics.throughput_per_hour:.2f}",
    "vehicles/hour",
)

print(
    "Average cycle time:",
    f"{metrics.average_cycle_time:.2f}s",
)

print(
    "Takt adherence:",
    f"{metrics.takt_adherence * 100:.1f}%",
)

print(
    "Average health:",
    f"{metrics.average_health * 100:.1f}%",
)

print(
    "Average queue:",
    f"{metrics.average_queue:.2f}",
)

print(
    "Bottlenecks:",
    metrics.bottleneck_count,
)

print(
    "Line health:",
    f"{metrics.line_health * 100:.1f}%",
)
