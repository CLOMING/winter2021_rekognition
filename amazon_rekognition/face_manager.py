from random import random
from typing import List, Tuple
from uuid import uuid4
from amazon_rekognition import index_faces
from amazon_rekognition import external_id_db


from amazon_rekognition import AmazonImage
from amazon_rekognition.utils import face
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
        
        # TODO1
        face_searcher=FaceSearcher(image=image,max_faces=1)
        searcher_responses=face_searcher.get_response()

        # faceMatch 존재할 때 (얼굴 이미 등록)
        if not not searcher_responses['FaceMatches'] :
            raise ValueError('face is already existed.')

        
        # TODO2
        face_indexer=FaceIndexer(image=image,external_image_id=external_id)
        indexer_responses=face_indexer.get_response()

        # index face 안됐을 때 (얼굴 등록 안됨)
        if not indexer_responses['ExternalImageId']:
            raise ValueError("face Indexing error")
        

        # TODO3
        external_id_db=ExternalIdDb()
        item=external_id_db.create(user_id=external_id,name=name)

        # 이미 존재 
        if not item:
            raise ValueError("item is already existed in table")
        
        
        #TODO4
        return external_id,face_searcher['FaceMatches'][0]


        # TODO: 1. image의 얼굴 인식
        # TODO: 2. 얼굴 인식 결과의 ExternalImageId가 없다면 FaceIndexer를 사용해 얼굴을 등록 (???)
        # TODO: 3. FaceIndexer를 통해 얼굴이 등록되었다면 그 ExternalImageId와 name을 db에 등록
        # TODO: 4. externalImageId, face를 반환

    def add_all_faces(
        self,
        image: AmazonImage,
    ) -> List[Tuple[str, Face]]:
        face_searcher=FaceSearcher()

        for i in len(face_searcher.get_response()):
            self.add_face()
        # TODO: 사진 상의 모든 얼굴을 등록, 이름은 random으로 부여
        

    def search_face(
        self,
        image: AmazonImage,
    ) -> List[FaceMatch]:
        face_searcher=FaceSearcher(image=image)
        face_matches=face_searcher.get_response()['FaceMatches'] #약간 코드 이상한 것 같음
        # TODO: 얼굴 인식한 결과를 return
        

    def update_name(
        self,
        image: AmazonImage,
        name: str
    ) -> Tuple[str,Face]:
        face_searcher=FaceSearcher()
        face_matches=face_searcher.get_response()['FaceMatches']
        face=face_matches[0]


        external_id_db=ExternalIdDb()
        external_id_db.update(user_id=face['ExternalImageID'],new_name=name)

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

        feature=['게으른','당돌한','행복한','까칠한','귀여운','수줍은','다정한','엉뚱한','나른한']
        animal=['펭귄','쿼카','알파카','나무늘보','레서팬더','사막여우','코끼리', '강아지']
        numList=list(range(1000)) 
        nickname = random.choice(feature)+random.choice(animal)+str(random.choice(numList)).zfill(3)
        return nickname

        