from app.twin.event import TelemetryEvent
from app.twin.manager import DigitalTwinManager


class EventProcessor:

    def __init__(
        self,
        twin: DigitalTwinManager,
    ):
        self.twin = twin

    def process(
        self,
        event: TelemetryEvent,
    ) -> None:

        factory = self.twin.state.factory

        station = factory.get_station(event.station_id)

        if station is None:
            raise ValueError(f"Unknown station: {event.station_id}")

        station.cycle_time = event.cycle_time
        station.temperature = event.temperature
        station.vibration = event.vibration
        station.torque = event.torque
        station.queue_length = event.queue_length
        station.sensor_available = event.sensor_available

        station.update_health()

        self.twin.state.last_updated = event.timestamp

        self.twin.advance(update_timestamp=False)
