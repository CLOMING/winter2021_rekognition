from dataclasses import dataclass

import boto3

class ExternalIdDb:

    def __init__(self) -> None:
        # self.db = boto3.resource
        # TODO: Dynamodb 객체 초기화
        pass

    def create_table(self):
        # TODO: Table 생성
        # TODO: DocComment 남기기
        pass

    def delete_table(self):
        # TODO: Table 삭제
        # TODO: DocComment 남기기
        pass

    def create(
        self,
        user_id: str,
        name: str,
    ) -> :
        # TODO: Table에 name, user_id 추가
        # TODO: DocComment 남기기
        # TODO: put_item의 결과를 Dataclass 형태로 담아서 return
        pass

    def read(
        self,
        user_id: str,
    ) -> :
        # TODO: Table에서 user_id로 검색한 결과를 반환
        # TODO: 검색해 찾은 name을 return, 검색한 결과가 없다면 error throw
        pass

    def update(
        self,
        user_id: str,
        new_name: str,
    ) -> :
        # TODO: user_id의 name을 new_name으로 변경
        # TODO: 결과를 dataclass로 wrapping 해서 반환

    def delete(
        self, 
        user_id: str,
    ) -> :
        # TODO: Table에서 user_id를 삭제
        # TODO: 결과를 datacalss를 사용해서 wrapping 해서 return