from typing import List, Tuple
from uuid import uuid4

from amazon_rekognition import AmazonImage
from external_id_db import ExternalIdDb
from index_faces import FaceIndexer
from search_faces_by_image import FaceMatch, FaceSearcher
from utils.face import *
from utils.measure_time import *


class FaceManager:

    def __init__(self) -> None:
        self.db = ExternalIdDb()

    def add_face(
        self,
        image: AmazonImage,
        name: Optional[str],
    ) -> Tuple[str, Face]:
        external_id = self._create_external_id()
        
        if not name:
            name = self._create_name()

        # TODO: 1. image의 얼굴 인식
        # TODO: 2. 얼굴 인식 결과의 ExternalImageId가 없다면 FaceIndexer를 사용해 얼굴을 등록
        # TODO: 3. FaceIndexer를 통해 얼굴이 등록되었다면 그 ExternalImageId와 name을 db에 등록
        # TODO: 4. externalImageId, face를 반환
        pass

    def add_all_faces(
        self,
        image: AmazonImage,
    ) -> List[Tuple[str, Face]]:
        # TODO: 사진 상의 모든 얼굴을 등록, 이름은 random으로 부여
        pass

    def search_face(
        self,
        image: AmazonImage,
    ) -> List[FaceMatch]:
        # TODO: 얼굴 인식한 결과를 return
        pass

    def update_name(
        self,
        image: AmazonImage,
        name: str
    ) -> :
        # TODO: 이름을 업데이트하여 결과를 반환
        pass


    def _create_external_id(self) -> str:
        return str(uuid4())

    def _create_name(self) -> str:
        # TODO: '~~한 ~~ ' 형태의 임의의 이름을 생성 ex) '까칠한 하트병정 001'
        # 뒤의 숫자는 3자리 랜덤 숫자
        pass