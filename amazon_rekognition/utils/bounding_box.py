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


def calculate_IoU(  #Intersection over Union
    boxA: Tuple[int, int, int, int],
    boxB: Tuple[int, int, int, int],
) -> float:
    inter_left = max(boxA[0], boxB[0])
    inter_right = min(boxA[1], boxB[1])
    inter_top = max(boxA[2], boxB[2])
    inter_bottom = min(boxA[3], boxB[3])

    inter_area = max(0, inter_right - inter_left) * max(
        0, inter_bottom - inter_top)

    boxA_area = (boxA[1] - boxA[0]) * (boxA[3] - boxA[2])
    boxB_area = (boxB[1] - boxB[0]) * (boxB[3] - boxB[2])

    iou = inter_area / float(boxA_area + boxB_area - inter_area)

    return iou
