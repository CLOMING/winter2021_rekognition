from math import floor, ceil
import random
from turtle import width
from typing import List, Tuple
from uuid import uuid4

import cv2
import numpy as np

from amazon_rekognition import AmazonImage
from detect_faces import FaceDetector, FaceDetail
from external_id_db import ExternalIdDb
from index_faces import FaceIndexer
from search_faces_by_image import FaceMatch, FaceSearcher
from utils.face import *
from utils.measure_time import *


class FaceManager:

    def __init__(self) -> None:
        self.db = ExternalIdDb()

    def get_faces(
        self,
        image: AmazonImage,
    ) -> List[FaceDetail]:
        pass

    def add_face(
        self,
        image: AmazonImage,
        name: Optional[str] = None,
    ) -> Tuple[str, Face]:
        external_id = self._create_external_id()

        if not name:
            name = self._create_name()

        face_searcher = FaceSearcher(image=image, max_faces=1)
        face_matches = face_searcher.run()

        if not not face_matches:
            raise ValueError('face is already existed.')

        face_indexer = FaceIndexer(image=image, external_image_id=external_id)
        faces = face_indexer.run()

        if not faces:
            raise ValueError("face Indexing error")

        external_id_db = ExternalIdDb()
        item = external_id_db.create(user_id=external_id, name=name)

        if not item:
            raise ValueError("item is already existed in table")

        return external_id, faces[0]

    def add_all_faces(
        self,
        image: AmazonImage,
    ) -> List[Tuple[str, Face]]:
        face_detector = FaceDetector(image=image)
        faces = face_detector.run()

        encoded_img = np.fromstring(image.bytes, dtype=np.uint8)
        img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        img_width = img.shape[1]
        img_height = img.shape[0]

        for face in faces:
            bounding_box = face.bounding_box

            left = bounding_box.left
            top = bounding_box.top
            width = bounding_box.width
            height = bounding_box.height

            cropped_img = img[floor(img_height * top):ceil(img_height *
                                                           (top + height)),
                              floor(img_width * left):ceil(img_width *
                                                           (left + width))]
            self.add_face(AmazonImage.from_ndarray(cropped_img))
  
    def search_face(
        self,
        image: AmazonImage,
    ) -> List[FaceMatch]:
        face_searcher = FaceSearcher(image=image)
        face_matches = face_searcher.run()
        # TODO: 얼굴 인식한 결과를 return

    def update_name(self, image: AmazonImage, name: str) -> Tuple[str, Face]:
        face_searcher = FaceSearcher()
        face_matches = face_searcher.run()
        face = face_matches[0]

        external_id_db = ExternalIdDb()
        external_id_db.update(user_id=face['ExternalImageID'], new_name=name)

        return name, face
        # TODO: 이름을 업데이트하여 결과를 반환
        # image얼굴 검색, id 찾고 , name 바꾸기

    def _create_external_id(self) -> str:
        return str(uuid4())

    def _create_name(self) -> str:
        """
        create name randomly (feature + animal + num)
        """
        # TODO: '~~한 ~~ ' 형태의 임의의 이름을 생성 ex) '까칠한 하트병정 001'
        # 뒤의 숫자는 3자리 랜덤 숫자

        feature = [
            '게으른', '당돌한', '행복한', '까칠한', '귀여운', '수줍은', '다정한', '엉뚱한', '나른한'
        ]
        animal = ['펭귄', '쿼카', '알파카', '나무늘보', '레서팬더', '사막여우', '코끼리', '강아지']
        numList = list(range(1000))
        nickname = random.choice(feature) + random.choice(animal) + str(
            random.choice(numList)).zfill(3)
        return nickname
