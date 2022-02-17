from dataclasses import dataclass
from typing import Dict, List

from utils.bounding_box import BoundingBox
from utils.measure_time import *
from amazon_rekognition import AmazonImage, AmazonRekognition
from pprint import pprint


@dataclass(frozen=True)
class FaceDetail:
    confidence: float
    bounding_box: BoundingBox

    def parse(data: Dict):
        return FaceDetail(
            confidence=data['Confidence'],
            bounding_box=BoundingBox.parse(data['BoundingBox']),
        )


class FaceDetector(AmazonRekognition[List[FaceDetail]]):

    def __init__(
        self,
        image: AmazonImage,
    ) -> None:
        super().__init__(image)

    def get_response(self) -> List[Dict]:
        return self.client.detect_faces(Image={
            'Bytes': self.image.bytes,
        }, )

    def parse_result(self, response: Dict) -> List[FaceDetail]:
        return [
            FaceDetail.parse(face_details)
            for face_details in response['FaceDetails']
        ]


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()
    parser.add_argument('--path', required=True)

    args = parser.parse_args()

    image_path = args.path

    detect_person = FaceDetector(image=AmazonImage.from_file(image_path))

    res = detect_person.run()

    pprint(res)
