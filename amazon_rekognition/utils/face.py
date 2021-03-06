from dataclasses import dataclass
from typing import Dict, Optional

from .bounding_box import BoundingBox


@dataclass
class Face:
    bounding_box: BoundingBox
    confidence: float
    external_image_id: Optional[str]
    face_id: str
    image_id: str

    def parse(data: Dict):
        return Face(
            bounding_box=BoundingBox.parse(data['BoundingBox']),
            confidence=data['Confidence'],
            face_id=data["FaceId"],
            image_id=data["ImageId"],
            external_image_id=data['ExternalImageId']
            if 'ExternalImageId' in data else None,
        )
