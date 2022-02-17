from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, TypeVar

import cv2
import boto3
import numpy

from utils import get_image_bytes, measure_time

T = TypeVar('T')


class AmazonImage:

    def __init__(
        self,
        image: bytes,
    ) -> None:
        if not image:
            raise ValueError("`image` must not be `None`!")

        self.__bytes = image

    @classmethod
    def from_file(cls, path: str):
        image = get_image_bytes(path)

        return cls(image)

    @classmethod
    def from_ndarray(cls, image_array: numpy.ndarray):
        image = cv2.imencode('.jpg', image_array)[1].tobytes()

        return cls(image)

    @property
    def bytes(self) -> bytes:
        return self.__bytes


class AmazonRekognition(Generic[T], metaclass=ABCMeta):

    def __init__(
        self,
        image: AmazonImage,
    ) -> None:
        self.image = image
        self.client = boto3.client('rekognition')

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
