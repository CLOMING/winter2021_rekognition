from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from boto3.dynamodb.conditions import Attr
import boto3


@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    face_ids: List[str]

    @classmethod
    def parse(cls, data: Dict):
        return User(user_id=data['user_id'],
                    name=data['name'],
                    face_ids=data['face_ids'])

    def copy_with(
        self,
        name: Optional[str] = None,
        face_ids: Optional[List[str]] = None,
    ):
        return User(user_id=self.user_id,
                    name=name or self.name,
                    face_ids=face_ids or self.face_ids)


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

        if self.data:
            error_message += f'\n{self.data}'

        return error_message


class UserDatabaseUserNotExistException(UserDatabaseException):

    def __init__(self, user_id) -> None:
        super().__init__(
            'user_id is not exist',
            {'user_id': user_id},
        )


class UserDatabaseUserAlreadExistException(UserDatabaseException):

    def __init__(self, user_id) -> None:
        super().__init__(
            'user_id is already exist',
            {'user_id': user_id},
        )


class UserDatabase:
    __service_name = 'dynamodb'
    __region_name = 'ap-northeast-2'
    __table_name = 'Users'
    __db = boto3.resource(
        __service_name,
        region_name=__region_name,
    )

    def __init__(self) -> None:
        self.table = UserDatabase.__db.Table(UserDatabase.__table_name)

    @classmethod
    def create_table(cls):
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
                    'AttributeName': 'user_id',  #External Id 
                    'AttributeType': 'S',  #string
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            },
        )

    @classmethod
    def delete_table(cls):
        UserDatabase.__db.Table(UserDatabase.__table_name).delete()

    def create(self, user: User) -> None:
        is_exist: bool
        try:
            self.read(user.user_id)
        except UserDatabaseUserNotExistException:
            is_exist = False
        else:
            is_exist = True

        if is_exist:
            raise UserDatabaseUserAlreadExistException(user.user_id)

        self.table.put_item(Item={
            'user_id': user.user_id,
            'name': user.name,
            'face_ids': user.face_ids
        })

    def read(self, user_id: str) -> User:
        res = self.table.get_item(Key={'user_id': user_id})

        if not ('Item' in res):
            raise UserDatabaseUserNotExistException(user_id)

        return User.parse(res['Item'])

    def update(self, user: User, new_name: str):
        is_exist: bool
        try:
            self.read(user.user_id)
        except UserDatabaseUserNotExistException:
            is_exist = False
        else:
            is_exist = True

        if not is_exist:
            raise UserDatabaseUserNotExistException(user.user_id)

        self.table.put_item(Item={
            'user_id': user.user_id,
            'name': new_name,
            'face_ids': user.face_ids
        }, )

    def delete(self, user_id: str):
        is_exist: bool
        try:
            self.read(user_id)
        except UserDatabaseUserNotExistException:
            is_exist = False
        else:
            is_exist = True

        if not is_exist:
            raise UserDatabaseUserNotExistException(user_id)

        self.table.delete_item(Key={'user_id': user_id})

    def search_by_name(self, name: str) -> List[User]:
        res = self.table.scan(FilterExpression=Attr('name').eq(name))
        # TODO: use query instead of scan

        return [User.parse(item) for item in res['Items']]

    def search_by_face_id(self, face_id: str) -> User:
        res = self.table.scan(
            FilterExpression=Attr('face_ids').contains(face_id))
        # TODO: use query instead of scan

        return [User.parse(item) for item in res['Items']]


if __name__ == '__main__':
    from pprint import pprint
    user_db = UserDatabase()
    user = User('uuid', '유재석', ['123123', '111111'])
    res = user_db.search_by_face_id(user.face_ids)
    pprint(res)
