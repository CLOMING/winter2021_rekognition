from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class BoundingBox:
    height: float
    width: float
    top: float
    left: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top - self.height

    def parse(data: Dict):

        return BoundingBox(
            height=data['Height'],
            width=data['Width'],
            top=data['Top'],
            left=data['Left'],
        )