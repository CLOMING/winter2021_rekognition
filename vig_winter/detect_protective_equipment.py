from argparse import ArgumentParser
from datetime import datetime
import io
from pprint import pprint
from typing import Optional

import boto3
from PIL import Image


class TimeDecorator:

    def __init__(self, f):

        self.func = f

    def __call__(self, *args, **kwargs):

        name = self.func.__name__

        start = datetime.now()

        print(f'[{name} start]')

        result = self.func(*args, **kwargs)

        end = datetime.now()

        print(f'[{name} end] {end - start}')

        return result


@TimeDecorator
def detect_mask(
    image_path: str,
    confidence: float,
):
    image_bytes: Optional[bytearray] = None
    with open(image_path, 'rb') as image:
        image_bytes = bytearray(image.read())

    if not image_bytes:
        return None

    client = boto3.client('rekognition')
    response = client.detect_protective_equipment(
        Image={'Bytes': image_bytes},
        SummarizationAttributes={
            'MinConfidence': confidence,
            'RequiredEquipmentTypes': ['FACE_COVER']
        },
    )

    pprint(response, compact=True)


@TimeDecorator
def read_image(image_path: str) -> Optional[bytearray]:
    # image_bytes: Optional[bytearray] = None
    # with open(image_path, 'rb') as image:
    #     image_bytes = bytearray(image.read())

    # return image_bytes

    image_bytes: Optional[bytearray] = None

    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        stream = io.BytesIO()
        image.save(stream, quality=25, format=image.format)
        image_bytes = stream.getvalue()
    image.close()

    return image_bytes


@TimeDecorator
def call_rekognition(image_bytes: bytearray, confidence: float) -> None:
    client = boto3.client('rekognition')
    response = client.detect_protective_equipment(
        Image={'Bytes': image_bytes},
        SummarizationAttributes={
            'MinConfidence': confidence,
            'RequiredEquipmentTypes': ['FACE_COVER']
        },
    )

    pprint(response)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('--path', required=True)
    parser.add_argument('--confidence')

    args = parser.parse_args()

    image_path = args.path
    confidence = float(args.confidence) if args.confidence else 80

    image_bytes: bytearray = read_image(image_path)
    call_rekognition(image_bytes, confidence)

    # detect_mask(image_path, confidence)