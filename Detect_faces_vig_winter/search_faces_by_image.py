from argparse import ArgumentParser
from dataclasses import dataclass
import io
from pprint import pprint
from typing import Dict

import boto3
from PIL import Image

import utils


@dataclass
class Face:
    bounding_box: utils.BoundingBox
    confidence: float
    external_image_id: str
    face_id: str
    image_id: str

    def parse(data: Dict):
        return Face(
            bounding_box=utils.BoundingBox.parse(data['BoundingBox']),
            confidence=data['Confidence'],
            external_image_id=data['ExternalImageId'],
            face_id=data["FaceId"],
            image_id=data["ImageId"],
        )


@dataclass
class FaceMatch:
    face: Face
    similarity: float

    def parse(data: Dict):
        return FaceMatch(
            face=Face.parse(data["Face"]),
            similarity=data["Similarity"],
        )


class FaceSearcher:

    def __init__(
        self,
        image_path: str,
        threshold: float = 70.0,
        max_faces: int = 2,
    ) -> None:
        self.image_path = image_path
        self.threshold = threshold
        self.max_faces = max_faces

    @utils.measure_time
    def run(self) -> list[FaceMatch]:
        self.read_image()
        return self.call_rekognition()

    @utils.measure_time
    def read_image(self) -> bytearray:
        try:
            self.image_bytes
        except AttributeError:
            pass
        else:
            if not (self.image_bytes == None):
                return self.image_bytes

        image_bytes: bytearray

        with open(self.image_path, 'rb') as image_file:
            image = Image.open(image_file)
            stream = io.BytesIO()
            image.save(stream, quality=25, format=image.format)
            image_bytes = stream.getvalue()
            image.close()

        if image_bytes == None:
            raise ValueError("image_bytes is None")

        self.image_bytes = image_bytes
        return image_bytes

    @utils.measure_time
    def call_rekognition(self) -> list[FaceMatch]:
        try:
            self.image_bytes
        except AttributeError:
            self.read_image()
        else:
            if self.image_bytes == None:
                self.read_image()

        client = boto3.client('rekognition')
        response = client.search_faces_by_image(
            CollectionId='Maskless_Collection',
            Image={'Bytes': self.image_bytes},
            FaceMatchThreshold=self.threshold,
            MaxFaces=self.max_faces,
        )

        return [FaceMatch.parse(match) for match in response['FaceMatches']]

        face_matches = []

        for data in response['FaceMatches']:
            face_match = FeceMatch.parse(data)
            face_matches.append(face_match)

        return face_matches


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('--path', required=True)
    parser.add_argument('--threshold', default=70)
    parser.add_argument('--max_faces', default=2)
    parser.add_argument('--measure_time', action='store_true')

    args = parser.parse_args()

    image_path = args.path
    threshold = float(args.threshold) if args.threshold else 70
    max_faces = int(args.max_faces) if args.max_faces else 2

    utils.enable_measure_time(
    ) if args.measure_time == True else utils.disable_measure_time()

    face_searcher = FaceSearcher(
        image_path=image_path,
        threshold=threshold,
        max_faces=max_faces,
    )
    face_matches = face_searcher.run()

    pprint(face_matches)
