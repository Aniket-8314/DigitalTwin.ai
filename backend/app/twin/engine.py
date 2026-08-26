import threading
import time

from app.simulation.dynamics import update_factory
from app.simulation.generator import generate_telemetry
from app.simulation.propagation import propagate_line_effects
from app.twin.event import TelemetryEvent
from app.twin.manager import DigitalTwinManager
from app.twin.processor import EventProcessor
from app.ml.live_predictor import LivePredictor
from app.ml.risk_score import (
    calculate_station_risk,
    risk_severity,
)

from app.ml.defect_risk import (
    defect_severity,
)
from app.ml.root_cause import (
    rank_root_causes,
)
from app.ml.recommendation import (
    generate_recommendations,
)


class TwinEngine:

    def __init__(
        self,
        twin: DigitalTwinManager,
        interval: float = 1.0,
        anomaly_model_path: str = ("data/anomaly_model.joblib"),
        bottleneck_model_path: str = ("data/bottleneck_model.joblib"),
        defect_model_path: str = ("data/defect_model.joblib"),
    ):
        self.twin = twin
        self.interval = interval

        self.processor = EventProcessor(twin)
        self.predictor = LivePredictor(
            anomaly_model_path=anomaly_model_path,
            bottleneck_model_path=(bottleneck_model_path),
            defect_model_path=(defect_model_path),
        )

        self.running = False
        self.thread = None
        self.previous_station_values = {}

    def step(self) -> None:

        factory = self.twin.state.factory

        # --------------------------------
        # Update simulated physical world
        # --------------------------------

        update_factory(
            factory,
            drift_station="S14",
        )

        # --------------------------------
        # Propagate line effects
        # --------------------------------

        propagate_line_effects(factory)

        # --------------------------------
        # Generate telemetry
        # --------------------------------

        vehicles = factory.vehicles

        if not vehicles:
            return

        vehicle = vehicles[self.twin.state.simulation_step % len(vehicles)]

        telemetry_records = generate_telemetry(
            factory,
            vehicle,
        )

        # --------------------------------
        # Feed telemetry into twin
        # --------------------------------

        for telemetry in telemetry_records:

            event = TelemetryEvent(
                timestamp=telemetry.timestamp,
                station_id=telemetry.station_id,
                vehicle_id=telemetry.vehicle_id,
                cycle_time=telemetry.cycle_time,
                temperature=telemetry.temperature,
                vibration=telemetry.vibration,
                torque=telemetry.torque,
                queue_length=telemetry.queue_length,
                sensor_available=(telemetry.sensor_available),
            )

            self.processor.process(event)
            station = factory.get_station(event.station_id)

            if station is None:
                continue

            previous = self.previous_station_values.get(station.station_id)

            if previous is not None:

                station.cycle_time_delta = station.cycle_time - previous["cycle_time"]

                station.vibration_delta = station.vibration - previous["vibration"]

                station.queue_delta = station.queue_length - previous["queue_length"]

                # station.torque_deviation = station.torque - previous["torque"]

            station.torque_deviation = station.torque - 40.0
            self.previous_station_values[station.station_id] = {
                "cycle_time": station.cycle_time,
                "vibration": station.vibration,
                "queue_length": station.queue_length,
                "torque": station.torque,
            }
            prediction = self.predictor.update(factory.get_station(event.station_id))
            event_vehicle = next(
                (v for v in factory.vehicles if v.vehicle_id == event.vehicle_id),
                None,
            )

            if prediction is not None:

                station = factory.get_station(event.station_id)

                if station is None:
                    continue

                station.anomaly_score = prediction["anomaly_score"]

                station.anomaly_severity = prediction["anomaly_severity"]

                station.bottleneck_probability = prediction["bottleneck_probability"]
                station.risk_score = calculate_station_risk(
                    station.anomaly_score,
                    station.bottleneck_probability,
                )

                if event_vehicle is not None:
                    event_vehicle.defect_probability = prediction["defect_probability"]
                    event_vehicle.defect_severity = defect_severity(
                        event_vehicle.defect_probability
                    )

                station.risk_severity = risk_severity(station.risk_score)
                station.root_causes = rank_root_causes(station)
                station.recommendations = generate_recommendations(station)

    def _run(self) -> None:

        while self.running:

            try:

                self.step()

            except Exception as error:

                print(
                    "Twin engine error:",
                    error,
                )

            time.sleep(self.interval)

    def start(self) -> None:

        if self.running:
            return

        self.running = True

        self.twin.start()

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self.thread.start()

    def stop(self) -> None:

        self.running = False

        self.twin.stop()
