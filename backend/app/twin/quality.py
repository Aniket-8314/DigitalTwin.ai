from dataclasses import dataclass


@dataclass
class QualityGate:
    defect_threshold: float = 0.30

    inspected: int = 0
    defects_detected: int = 0

    def inspect(self, vehicle) -> bool:

        self.inspected += 1

        defect_found = vehicle.defect_risk >= self.defect_threshold

        if defect_found:
            self.defects_detected += 1

        return defect_found

    @property
    def defect_rate(self) -> float:

        if self.inspected == 0:
            return 0.0

        return self.defects_detected / self.inspected
