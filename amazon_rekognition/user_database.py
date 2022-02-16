from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3

from amazon_rekognition.external_id_db import ExternalIdDbNotExistException

@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    face_ids: List[str]

    @classmethod
    def parse(data: Dict):
        return User(
            user_id=data['UserId'],
            name=data['Name'],
            face_ids=[tmp for tmp in data['FaceIds']],
        )

    def copy_with(
        self,
        name: Optional[str] = None,
        face_ids: Optional[List[str]] = None,
    ):
        return User(
            user_id=self.user_id,
            name=name or self.name,
            face_ids=face_ids or self.face_ids,
        )


class UserDatabase:
    __service_name = 'dynamodb'
    __region_name = 'ap-northeast-2'
    __table_name = 'User'
    __db = boto3.resource(
        __service_name,
        region_name=__region_name,
    )

    def __init__(self) -> None:
        self.table = UserDatabase.__db.Table(UserDatabase.__table_name)

    @classmethod
    def create_table():
        UserDatabase.__db.create_table(
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
            },
        )

    @classmethod
    def delete_table():
        UserDatabase.__db.Table(UserDatabase.__table_name).delete()

    def create(self, user: User):
        is_exist:bool = False
        try:
            self.read(User.user_id)
        except ExternalIdDbNotExistException:
            is_exist=False
        else:
            is_exist=True

        table=self.__db.Table('Users')
        res=table.put_item(Item={
            'UserId':User.user_id,
            'UserName':User.name,
        })
        # read해서 존재 여부 체크 후 이미 사용중인 user_id라면 UserDatabaseUserAlreadExistException raise
        

    def read(self, user_id: str) -> User:
        table=self.__db.Table('Users')
        res=table.get_item(Key={'UserID':user_id})

        if not ('Item' in res):
            raise ExternalIdDbNotExistException(user_id)

        return res['Item']['UserName']
        # item에 user 없는지 확인해서 exception -> UserDatabaseUserNotExistException
        

    def update(self, user: User):
        try:
            self.read(user.user_id)
        except:
            # TODO

        self.create(user)
    

    def delete(self, user_id: str):
        # read해서 존재 여부 체크 후 없다면 UserDatabaseUserNotExistException raise
        pass

    def search_by_name(self, name: str) -> User:
        # name으로 user 찾기

    def search_by_face_id(self, face_id: str) -> User:
        # face_id 로 user 찾기




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


class UserDatabaseUserNotExistException(UserDatabaseException):
    # TODO


class UserDatabaseUserAlreadExistException(UserDatabaseException):

    def __init__(self, user_id, str) -> None:
        super().__init__(
            'user_id is already exist',
            {'user_id': user_id},
        )