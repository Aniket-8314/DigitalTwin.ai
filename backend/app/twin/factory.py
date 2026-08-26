from dataclasses import dataclass, field
from typing import List

from app.twin.buffer import Buffer
from app.twin.station import Station
from app.twin.vehicle import Vehicle
from app.twin.quality import QualityGate


@dataclass
class Factory:
    stations: List[Station] = field(default_factory=list)
    vehicles: List[Vehicle] = field(default_factory=list)
    buffers: List[Buffer] = field(default_factory=list)
    quality_gate: QualityGate = field(default_factory=QualityGate)

    def add_station(self, station: Station) -> None:
        self.stations.append(station)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicles.append(vehicle)

    def add_buffer(self, buffer: Buffer) -> None:
        self.buffers.append(buffer)

    def get_station(self, station_id: str) -> Station | None:
        for station in self.stations:
            if station.station_id == station_id:
                return station

        return None

    def get_vehicle(self, vehicle_id: str) -> Vehicle | None:
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                return vehicle

        return None

    def get_buffer(self, buffer_id: str) -> Buffer | None:
        for buffer in self.buffers:
            if buffer.buffer_id == buffer_id:
                return buffer

        return None

    @property
    def station_count(self) -> int:
        return len(self.stations)

    @property
    def vehicle_count(self) -> int:
        return len(self.vehicles)

    @property
    def buffer_count(self) -> int:
        return len(self.buffers)

    @property
    def average_cycle_time(self) -> float:
        if not self.stations:
            return 0.0

        return sum(station.cycle_time for station in self.stations) / len(self.stations)

    @property
    def bottleneck_stations(self) -> list[Station]:
        return [station for station in self.stations if station.is_bottleneck()]
