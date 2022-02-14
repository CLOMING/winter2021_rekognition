from dataclasses import dataclass
from typing import Any, Optional

import boto3


class ExternalIdDb:

    def __init__(self) -> None:
        self.db = boto3.resource('dynamodb', region_name='ap-northeast-2')

    def create_table(self):
        table = self.db.create_table(
            TableName='Faces',
            KeySchema=[
                {
                    'AttributeName': 'UserId',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'UserId',  #External Id 
                    'AttributeType': 'S',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        return table

    def delete_table(self):
        table = self.db.Table('Faces')
        table.delete()

    def create(
        self,
        user_id: str,
        name: str,
    ) -> bool:
        is_exist: bool = False
        try:
            self.read(user_id)
        except ExternalIdDbNotExistException:
            is_exist = False
        else:
            is_exist = True

        if is_exist:
            return False

        table = self.db.Table('Faces')
        res = table.put_item(Item={
            'UserId': user_id,
            'UserName': name,
        })
        return True

    def read(
        self,
        user_id: str,
    ):
        table = self.db.Table('Faces')
        res = table.get_item(Key={'UserId': user_id})

        if not ('Item' in res):
            raise ExternalIdDbNotExistException(user_id)

        return res['Item']['UserName']

    def update(
        self,
        user_id: str,
        new_name: str,
    ) -> bool:

        delete = self.delete(user_id)

        res = self.create(user_id, new_name)
        return True

    def delete(
        self,
        user_id: str,
    ) -> bool:
        is_exist: bool = False
        try:
            self.read(user_id)
        except ExternalIdDbNotExistException:
            is_exist = False
        else:
            is_exist = True

        if not is_exist:
            return False

        table = self.db.Table('Faces')
        res = table.delete_item(Key={'UserId': user_id}, )
        return True


class ExternalIdDbException(Exception):

    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.data = data

    def __str__(self) -> str:
        error_message: str = f'[ExternalIdDbError] {self.message}'

        if not self.data:
            error_message += f'\n{self.data}'

        return error_message


class ExternalIdDbAlreadExistException(ExternalIdDbException):

    def __init__(self, user_id: str) -> None:
        super().__init__(
            'user_id is alread exist.',
            {'user_id': user_id},
        )


class ExternalIdDbNotExistException(ExternalIdDbException):

    def __init__(self, user_id: str):
        super().__init__(
            'user_id is not exist.',
            {'user_id': user_id},
        )
