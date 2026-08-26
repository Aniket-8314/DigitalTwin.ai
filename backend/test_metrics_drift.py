from app.simulation.dynamics import (
    update_factory,
)

from app.simulation.generator import (
    create_factory,
)

from app.simulation.propagation import (
    propagate_line_effects,
)

from app.twin.metrics import (
    calculate_metrics,
)


factory = create_factory()


print("DIGITALTWIN.AI")
print("Metric Degradation Test")
print("=" * 55)


for step in range(20):

    update_factory(
        factory,
        drift_station="S14",
    )

    propagate_line_effects(factory)

    metrics = calculate_metrics(factory)

    print(f"\nStep {step + 1}")

    print(
        "Throughput:",
        f"{metrics.throughput_per_hour:.1f}/hr",
    )

    print(
        "Avg cycle:",
        f"{metrics.average_cycle_time:.1f}s",
    )

    print(
        "Takt adherence:",
        f"{metrics.takt_adherence * 100:.1f}%",
    )

    print(
        "Line health:",
        f"{metrics.line_health * 100:.1f}%",
    )

    print(
        "Bottlenecks:",
        metrics.bottleneck_count,
    )
