from dataclasses import dataclass
from typing import Dict, List

from utils.bounding_box import BoundingBox
from utils.measure_time import *
from amazon_rekognition import *


@dataclass(frozen=True)
class Person:
    confidence: float
    bounding_box: BoundingBox

    def parse(data: Dict):
        return Person(
            confidence=data['Confidence'],
            bounding_box=BoundingBox.parse(data['Instance'][0]['BoundingBox']),
        )


class DetectPerson(AmazonRekognition[List[Person]]):

    def __init__(
        self,
        image: AmazonImage,
    ) -> None:
        super().__init__(image)

    def get_response(self) -> List[Dict]:
        return self.client.detect_labels(Image={
            'Bytes': self.image.bytes,
        }, )

    def parse_result(self, response: Dict) -> List[Person]:
        labels = response['Labels']
        result: List[Person] = []
        for label in labels:
            if not (label['name'] == 'Person'):
                continue

            instances = label['Instance']

            if not (len(instances) == 1):
                continue

            if len(instances) == 1 and "BoundingBox" in instances[0]:
                pass

            result.append(Person())

        return result


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()
    parser.add_argument('--path', required=True)

    args = parser.parse_args()

    image_path = args.path

    detect_person = DetectPerson(image=AmazonImage.from_file(image_path))

    res = detect_person.run()

    pprint(res)
