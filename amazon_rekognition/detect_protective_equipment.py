from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from amazon_rekognition import AmazonRekognition
import utils


@dataclass(frozen=True)
class CoversBodyPart:
    confidence: float
    value: bool

    def parse(data: Dict):
        return CoversBodyPart(
            confidence=data['Confidence'],
            value=data['Value'],
        )


@dataclass(frozen=True)
class EquipmentDetection:
    confidence: float
    bounding_box: utils.BoundingBox
    covers: CoversBodyPart
    type: str

    def parse(data: Dict):
        return EquipmentDetection(
            confidence=data['Confidence'],
            bounding_box=utils.BoundingBox.parse(data['BoundingBox']),
            covers=CoversBodyPart.parse(data['CoversBodyPart']),
            type=data['Type'],
        )


@dataclass(frozen=True)
class BodyPart:
    confidence: float
    equipment_detections: List[EquipmentDetection]
    name: str

    def parse(data: Dict):
        return BodyPart(
            confidence=data['Confidence'],
            equipment_detections=[
                EquipmentDetection.parse(tmp)
                for tmp in data['EquipmentDetections']
            ],
            name=data['Name'],
        )


class MaskStatus(Enum):
    UNKNOWN = 'UNKNOWN'
    WEARED = 'WEARED'
    NOT_WEARED = 'NOT_WEARED'


@dataclass(frozen=True)
class Person:
    bounding_box: utils.BoundingBox
    id: float
    confidence: float
    body_parts: List[BodyPart]

    @property
    def mask_status(self) -> MaskStatus:
        faces = [part for part in self.body_parts if part.name == 'FACE']

        if len(faces) != 1:
            return MaskStatus.UNKNOWN

        face = faces[0]

        masks = [
            equipment for equipment in face.equipment_detections
            if equipment.type == "FACE_COVER"
        ]

        if len(masks) != 1:
            return MaskStatus.NOT_WEARED

        mask = masks[0]

        if not mask.covers.value:
            return MaskStatus.NOT_WEARED

        return MaskStatus.WEARED

    def parse(data: Dict):
        return Person(
            bounding_box=utils.BoundingBox.parse(data['BoundingBox']),
            id=data['Id'],
            confidence=data['Confidence'],
            body_parts=[BodyPart.parse(tmp) for tmp in data['BodyParts']],
        )


class MaskDetector(AmazonRekognition[List[Person]]):

    def __init__(
        self,
        image_path: str,
        confidence: float = 80.0,
    ) -> None:
        super().__init__(image_path)
        self.confidence = confidence

    def get_response(self) -> Dict:
        return self.client.detect_protective_equipment(
            Image={'Bytes': self.image_bytes},
            SummarizationAttributes={
                'MinConfidence': confidence,
                'RequiredEquipmentTypes': ['FACE_COVER']
            },
        )

    def parse_result(self, response: Dict) -> List[Person]:
        return [Person.parse(person) for person in response['Persons']]


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()

    parser.add_argument('--path', required=True)
    parser.add_argument('--confidence', default=80)
    parser.add_argument('--measure_time', action='store_true')

    args = parser.parse_args()

    image_path = args.path
    confidence = float(args.confidence) if args.confidence else 80

    utils.enable_measure_time(
    ) if args.measure_time == True else utils.disable_measure_time()

    mask_detector = MaskDetector(image_path, confidence)
    persons = mask_detector.run()

    for person in persons:
        if person.mask_status == MaskStatus.WEARED:
            print(f'Person {person.id} wear a mask!')
        else:
            print(
                f'Person {person.id} does not wear a mask!({person.mask_status})'
            )
            pprint(person)