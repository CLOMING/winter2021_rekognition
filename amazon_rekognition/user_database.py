from dataclasses import dataclass
from typing import Any, List, Optional

import boto3


@dataclass
class User:
    user_id: str
    name: str
    face_ids: List[str]


class UserDatabase:
    __service_name = 'dynamodb'
    __region_name = 'ap-northeast-2'
    __table_name = 'User'

    def __init__(self) -> None:
        db = boto3.resource(
            UserDatabase.__service_name,
            region_name=UserDatabase.__region_name,
        )
        self.table = db.Table(UserDatabase.__table_name)

    @classmethod
    def create_table(self):  #self로 접근하는게 맞는지
        #  table = boto3.resource(
        #     UserDatabase.__service_name,
        #     region_name=UserDatabase.__region_name,
        # )
        table = self.db.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'name',  #External Id 
                    'AttributeType': 'S',  #string
                },
                {
                    'AttributeName': 'face_id',  #External Id 
                    'AttributeType': 'SS',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        # TableName 'User'로 설정
        # keySchema user_id
        # name: str, face_id: List[str]
        pass

    @classmethod
    def delete_table():
        db = boto3.resource(
            UserDatabase.__service_name,
            region_name=UserDatabase.__region_name,
        )
        db.Table(UserDatabase.__table_name).delete()

    def create(self, user_id: str, name: str):
        
        # put_item 한 res의 status code를 확인해서 200이 아니면 exception
        pass

    def read(self, user_id: str) -> User:
        # item에 user 없는지 확인해서 exception -> UserDatabaseUserNotExistException
        pass

    def delete(self, user_id: str):
        # res의 status code를 확인해서 진행
        pass


class UserDatabaseException(Exception):

    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.data = data

    def __str__(self) -> str:
        error_message: str = f'[UserDatabaseException] {self.message}'

        if not self.data:
            error_message += f'\n{self.data}'

        return error_message


class UserDatabaseUserAlreadExistException(UserDatabaseException):

    def __init__(self, user_id, str) -> None:
        super().__init__(
            'user_id is already exist',
            {'user_id': user_id},
        )