from dataclasses import dataclass
from typing import Dict, List

from amazon_rekognition import AmazonImage, AmazonRekognition
from utils import *


@dataclass
class FaceMatch:
    face: Face
    similarity: float

    def parse(data: Dict):
        return FaceMatch(
            face=Face.parse(data["Face"]),
            similarity=data["Similarity"],
        )


class FaceSearcher(AmazonRekognition[List[FaceMatch]]):

    def __init__(
        self,
        image: AmazonImage,
        threshold: float = 70.0,
        max_faces: int = 2,
    ) -> None:
        super().__init__(image)
        self.threshold = threshold
        self.max_faces = max_faces

    def get_response(self) -> Dict:
        return self.client.search_faces_by_image(
            CollectionId='Maskless_Collection',
            Image={'Bytes': self.image.bytes},
            FaceMatchThreshold=self.threshold,
            MaxFaces=self.max_faces,
        )

    def parse_result(self, response: Dict) -> List[FaceMatch]:
        return [FaceMatch.parse(match) for match in response['FaceMatches']]


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()

    parser.add_argument('--path', required=True)
    parser.add_argument('--threshold', default=70)
    parser.add_argument('--max_faces', default=2)
    parser.add_argument('--measure_time', action='store_true')

    args = parser.parse_args()

    image_path = args.path
    threshold = float(args.threshold) if args.threshold else 70
    max_faces = int(args.max_faces) if args.max_faces else 2

    if args.measure_time:
        enable_measure_time()
    else:
        disable_measure_time()

    face_searcher = FaceSearcher(
        image=AmazonImage.from_file(image_path),
        threshold=threshold,
        max_faces=max_faces,
    )
    face_matches = face_searcher.run()

    pprint(face_matches)
