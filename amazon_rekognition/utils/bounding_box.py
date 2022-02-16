from dataclasses import dataclass
from typing import Dict, Tuple


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
        return self.top + self.height

    def calculate_points(
        self,
        img_width: int,
        img_height: int,
    ) -> Tuple[int, int, int, int]:
        """
        (left, right, top, bottom): Tuple[int, int, int, int]
        """
        return (
            int(self.left * img_width),
            int(self.right * img_width),
            int(self.top * img_height),
            int(self.bottom * img_height),
        )

    def parse(data: Dict):

        return BoundingBox(
            height=data['Height'],
            width=data['Width'],
            top=data['Top'],
            left=data['Left'],
        )