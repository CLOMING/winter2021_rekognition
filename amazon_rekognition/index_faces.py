from argparse import ArgumentParser
from typing import List

from amazon_rekognition import AmazonRekognition
from utils import *


class FaceIndexer(AmazonRekognition[List[Face]]):

    def __init__(
        self,
        image: bytes,
        external_image_id: str,
    ) -> None:
        super().__init__(image)
        self.external_image_id = external_image_id

    def get_response(self) -> Dict:
        return self.client.index_faces(
            CollectionId='Maskless_Collection',
            Image={'Bytes': self.image},
            ExternalImageId=self.external_image_id,
            MaxFaces=1,
            QualityFilter='AUTO',
        )

    def parse_result(self, response: Dict) -> List[Face]:
        return [
            Face.parse(face_record['Face'])
            for face_record in response['FaceRecords']
        ]


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--id', required=True)

    args = parser.parse_args()

    image_path = args.path
    id = args.id

    face_indexer = FaceIndexer.from_file(
        image_path=image_path,
        external_image_id=id,
    )
    face = face_indexer.run()
    pprint(face)