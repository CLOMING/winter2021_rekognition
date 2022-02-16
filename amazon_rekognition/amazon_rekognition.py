from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, TypeVar

import boto3

from utils import get_image_bytes, measure_time

T = TypeVar('T')


class AmazonRekognition(Generic[T], metaclass=ABCMeta):

    def __init__(
        self,
        image_path: str,
    ) -> None:
        self.image_path = image_path
        self.client = boto3.client('rekognition')

    @measure_time
    def run(self) -> T:
        self.read_image()
        return self.call_rekognition()

    @measure_time
    def read_image(self, quality: int = 25) -> bytearray:
        try:
            self.image_bytes
        except AttributeError:
            pass
        else:
            if not (self.image_bytes == None):
                return self.image_bytes

        image_bytes = get_image_bytes(self.image_path, quality)

        self.image_bytes = image_bytes
        return image_bytes

    @measure_time
    def call_rekognition(self) -> T:
        try:
            self.image_bytes
        except AttributeError:
            self.read_image()
        else:
            if self.image_bytes == None:
                self.read_image()

        response = self.get_response()

        return self.parse_result(response)

    @abstractmethod
    def get_response(self) -> Dict:
        pass

    @abstractmethod
    def parse_result(self, response: Dict) -> T:
        pass
