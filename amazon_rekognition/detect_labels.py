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
            bounding_box=BoundingBox.parse(data['BoundingBox']),
        )


class PeopleDetector(AmazonRekognition[List[Person]]):

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
            if not (label['Name'] == 'Person'):
                continue

            instances = label['Instances']

            if len(instances) == 0: #없으면
                continue

            #1개 이상일 때 
            #instances는 1개 이상으로 나옴 
            for instance in instances:
                result.append(Person(instance))  

        return result


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()
    parser.add_argument('--path', required=True)

    args = parser.parse_args()

    image_path = args.path

    detect_person = PeopleDetector(image=AmazonImage.from_file(image_path))

    res = detect_person.run()

    pprint(res)
