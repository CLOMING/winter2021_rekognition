from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from boto3.dynamodb.conditions import Key, Attr
import boto3

@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    face_ids: List[str]

    @classmethod
    def parse(data: Dict):
        return User(
            user_id = data['ExternalId'],
            name = data['Name'],
            face_ids = data['FaceId']
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
    def create_table(self):
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
    def delete_table():
        UserDatabase.__db.Table(UserDatabase.__table_name).delete()

    def create(self, user: User):
        try:
            res = self.read(user.user_id)
        except UserDatabaseUserNotExistException:
            self.table.put_item(
                Item = {
                    'user_id': user.user_id,
                    'name': user.name,
                    'face_ids': user.face_ids
                }
            )
            return user
        else:
            if res['user_id'] == user.user_id:
                raise UserDatabaseUserAlreadExistException(user.user_id)
            
    def read(self, user_id: str) -> User:
        table = UserDatabase.__db.Table(UserDatabase.__table_name)

        res = table.get_item(Key={'user_id': user_id}) 
        if not('Item' in res):
            raise UserDatabaseUserNotExistException(user_id)
        else:
            return res['Item']


    #update의 case-> 없는 id일 수 있음.
    def update(self, user: User, new_name: str):     
        try:  
            res = self.read(user.user_id)   
        except UserDatabaseUserNotExistException as e: 
            raise e
        else:  
            self.table.put_item(
                Item = {
                    'user_id': user.user_id,
                    'name': new_name,
                    'face_ids': user.face_ids
                }
            )
            return {'user_id':user.user_id, 'name': new_name, 'face_ids': user.face_ids}

    def delete(self, user_id: str):
        # read해서 존재 여부 체크 후 없다면 UserDatabaseUserNotExistException raise
        try:
            res = self.read(user_id)
        except UserDatabaseUserNotExistException as e:
            raise e
        else:
            self.table.delete_item(
                Key={
                    'user_id': user_id
                    }
            )
            return 'delete complete'

    def search_by_name(self, name: str) -> User:
        #name으로 user 찾기 
        response = self.table.scan(
            FilterExpression = Attr('name').eq(name)
        )
        items = response['Items']
        return items

    def search_by_face_id(self, face_id: str) -> User:
        pass


    @classmethod
    def delete_table():
        UserDatabase.__db.Table(UserDatabase.__table_name).delete()



if __name__ == '__main__':
    from pprint import pprint
    user_db=UserDatabase()
    user = User('uuid', '유재석', ['123123','111111'])
    #res = user_db.create(user)
    #res = user_db.update(user,'유재석')
    #res = user_db.search_by_name('강호동')
    res = user_db.search_by_face_id(user.face_ids)
    #res = user_db.read('uuid')
    #res = user_db.delete('uuid')
    pprint(res)
