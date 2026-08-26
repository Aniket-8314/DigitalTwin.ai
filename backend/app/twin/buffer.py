from dataclasses import dataclass


@dataclass
class Buffer:
    buffer_id: str

    capacity: int = 20
    current_level: int = 0

    def add(self, amount: int = 1) -> None:
        self.current_level = min(
            self.capacity,
            self.current_level + amount,
        )

    def remove(self, amount: int = 1) -> None:
        self.current_level = max(
            0,
            self.current_level - amount,
        )

    @property
    def utilization(self) -> float:
        return self.current_level / self.capacity
