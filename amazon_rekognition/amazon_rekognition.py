from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, TypeVar

import cv2
import boto3
import numpy

from utils.image_helper import get_image_bytes
from utils.measure_time import measure_time

T = TypeVar('T')


class AmazonRekognition(Generic[T], metaclass=ABCMeta):

    def __init__(
        self,
        image: bytes,
    ) -> None:
        if not image:
            raise ValueError("`image` must not be `None`!")
        self.image = image
        self.client = boto3.client('rekognition')

    @classmethod
    def from_file(
        cls,
        image_path: str,
        *args,
        **kargs,
    ):
        image = get_image_bytes(image_path)

        return cls(image, *args, **kargs)

    @classmethod
    def from_ndarray(
        cls,
        image_array: numpy.ndarray,
        *args,
        **kargs,
    ):
        image = cv2.imencode('.jpg', image_array)[1].tobytes()

        return cls(image, *args, **kargs)

    @measure_time
    def run(self) -> T:
        return self.call_rekognition()

    @measure_time
    def call_rekognition(self) -> T:
        response = self.get_response()

        return self.parse_result(response)

    @abstractmethod
    def get_response(self) -> Dict:
        pass

    @abstractmethod
    def parse_result(self, response: Dict) -> T:
        pass
