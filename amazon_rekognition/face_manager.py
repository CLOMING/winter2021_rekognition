from math import floor, ceil
import random
from typing import Any, List, Tuple
from uuid import uuid4

import cv2
import numpy as np

from amazon_rekognition import AmazonImage
from detect_faces import FaceDetector, FaceDetail
from user_database import User, UserDatabase, UserDatabaseUserAlreadExistException
from index_faces import FaceIndexer
from search_faces_by_image import FaceMatch, FaceSearcher
from utils.face import *
from utils.measure_time import *


class FaceManager:

    def __init__(self) -> None:
        self.db = UserDatabase()

    def get_faces(
        self,
        image: AmazonImage,
    ) -> List[FaceDetail]:

        face_detector = FaceDetector(image=image)
        faces = face_detector.run()

        if not faces:
            raise FaceManagerExceptionFaceNotExistException

        return faces

    def search_face(
        self,
        image: AmazonImage,
    ) -> List[Tuple[FaceMatch, int, int]]:

        face_informations: List[Tuple[np.ndarray, int, int]]

        try:
            face_informations = self.crop_image(image)
        except FaceManagerExceptionFaceNotExistException as e:
            raise e

        result: List[Tuple[FaceMatch, int, int]] = []

        for face_information in face_informations:
            face_matches: FaceMatch
            try:
                face_matches = self.search_only_one_face(
                    AmazonImage.from_ndarray(face_information[0]))
            except FaceManagerExceptionFaceNotSearchedException:
                face_matches = None

            if not face_matches:
                continue

            result.append(
                [face_matches, face_information[1], face_information[2]])

        if not result:
            raise FaceManagerExceptionFaceNotSearchedException

        return result

    def search_only_one_face(
        self,
        image: AmazonImage,
    ) -> FaceMatch:
        face_searcher = FaceSearcher(image, max_faces=1)
        face_matches = face_searcher.run()

        if not face_matches:
            raise FaceManagerExceptionFaceNotSearchedException()

        return face_matches[0]

    def crop_image(
        self,
        image: AmazonImage,
    ) -> List[Tuple[np.ndarray, int, int]]:
        try:
            faces = self.get_faces(image)
        except FaceManagerExceptionFaceNotExistException as e:
            raise e

        encoded_img = np.fromstring(image.bytes, dtype=np.uint8)
        img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        img_height = img.shape[0]
        img_width = img.shape[1]

        new_images = []
        for face in faces:
            bounding_box = face.bounding_box

            left = bounding_box.left * img_width
            top = bounding_box.top * img_height
            width = bounding_box.width * img_width
            height = bounding_box.height * img_height

            cropped_img = img[floor(top):ceil(top + height),
                              floor(left):ceil(left + width)]
            new_images.append((cropped_img, left, top))

        return new_images

    def add_face(
        self,
        image: AmazonImage,
        name: Optional[str] = None,
        check_face_exist: bool = True,
    ) -> Tuple[str, Face]:

        if check_face_exist:
            try:
                self.get_faces(image)
            except FaceManagerExceptionFaceNotExistException as e:
                raise e

        external_id = self._create_external_id()
        if not name:
            name = self._create_name()

        face_matches: Optional[List[Tuple[FaceMatch, int, int]]]
        try:
            face_matches = self.search_face(image)
        except FaceManagerExceptionFaceNotSearchedException:
            face_matches = None

        if face_matches:
            raise FaceManagerExceptionFaceAlreadyExistException(
                face_matches[0][0].face.external_image_id)

        face_indexer = FaceIndexer(image=image, external_image_id=external_id)
        faces = face_indexer.run()
        if not faces:
            raise FaceManagerExceptionFaceIndexErrorException

        try:
            self.db.create(User(external_id, name, [faces[0].face_id]))
        except UserDatabaseUserAlreadExistException:
            raise FaceManagerExceptionItemAlreadyExistException(
                external_image_id=external_id)

        return external_id, faces[0]

    def add_all_faces(
        self,
        image: AmazonImage,
    ) -> List[Tuple[str, Face]]:
        try:
            self.get_faces(image)
        except FaceManagerExceptionFaceNotExistException as e:
            raise e

        cropped_images_details = self.crop_image(image)
        for cropped_image_details in cropped_images_details:
            cropped_image_ndarray = cropped_image_details[0]  #ndarray
            cropped_image = AmazonImage.from_ndarray(cropped_image_ndarray)
            try:
                print(self.add_face(cropped_image))
            except Exception as e:
                print(e)

    def update_name(self, image: AmazonImage, name: str) -> Tuple[str, Face]:

        try:
            self.get_faces(image)
        except FaceManagerExceptionFaceNotExistException as e:
            raise e

        try:
            face_informations = self.search_face(image)
        except FaceManagerExceptionFaceNotSearchedException as e:
            raise e

        if not len(face_informations) == 1:
            raise FaceManagerExceptionUpdateNameException(
                len(face_informations))

        face = face_informations[0][0].face
        user = self.db.read(face.external_image_id)
        self.db.update(user, new_name=name)

        return name, face

    def _create_external_id(self) -> str:
        return str(uuid4())

    def _create_name(self) -> str:
        """
        create name randomly (feature + animal + num)
        """
        feature = [
            '게으른', '당돌한', '행복한', '까칠한', '귀여운', '수줍은', '다정한', '엉뚱한', '나른한'
        ]
        animal = ['펭귄', '쿼카', '알파카', '나무늘보', '레서팬더', '사막여우', '코끼리', '강아지']
        numList = list(range(1000))
        nickname = random.choice(feature) + random.choice(animal) + str(
            random.choice(numList)).zfill(3)
        return nickname


class FaceManagerException(Exception):

    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.data = data

    def __str__(self) -> str:
        error_message: str = f'[FaceManagerException] {self.message}'

        if self.data:
            error_message += f'\n{self.data}'

        return error_message


class FaceManagerExceptionFaceAlreadyExistException(FaceManagerException):

    def __init__(self, external_image_id: str) -> None:
        super().__init__(
            'Face already exists in Collection',
            {'external_image_id': external_image_id},
        )


class FaceManagerExceptionFaceIndexErrorException(FaceManagerException):

    def __init__(self) -> None:
        super().__init__('Face Indexing Error')


class FaceManagerExceptionItemAlreadyExistException(FaceManagerException):

    def __init__(self, external_image_id: str, name: str) -> None:
        super().__init__(
            'Item Already Exists Error',
            {
                'external_image_id': external_image_id,
                'name': name,
            },
        )


class FaceManagerExceptionUpdateNameException(FaceManagerException):

    def __init__(self, face_count: int) -> None:
        super().__init__(
            'The number of face to update name is more than one : ',
            {'face_count': face_count})


class FaceManagerExceptionFaceNotSearchedException(FaceManagerException):

    def __init__(self) -> None:
        super().__init__('Face is not Searched in Collection.')


class FaceManagerExceptionFaceNotExistException(FaceManagerException):

    def __init__(self) -> None:
        super().__init__('Fail to Get Face, Because Face Not Exists')
