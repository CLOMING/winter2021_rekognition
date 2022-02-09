from cgitb import enable
from dataclasses import dataclass
from distutils.log import error
from boto3.dynamodb.conditions import Key
import boto3
from pprint import pprint
from utils.measure_time import *


class ExternalIdDb:

    def __init__(self, dynamodb=None) -> None:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        self.db = dynamodb

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
        }
    )
        return table

    def delete_table(self):
        table = self.db.Table('Faces')
        table.delete()

    def create(
        self,
        user_id: str,
        name: str,
    )  -> bool:
        read = self.read(user_id)
        if not read :
            return False  #ㅣ미 있는 것

        table = self.db.Table('Faces')
        res = table.put_item(
            Item = {
                'UserId': user_id,
                'UserName': name
            }
        )
        return True
    
    @measure_time
    def read(
        self,
        user_id: str,
    ):
        table = self.db.Table('Faces')
        res = table.get_item(
            Key={
                'UserId': user_id
            }
        )

        if not ('Item' in res):
            #raise ValueError('없는 UserId 입니다.')
            return False

        return res['Item']['UserName']
        

    def update(
        self,
        user_id: str,
        new_name: str,
    ) -> bool:

        delete = self.delete(user_id)
        if not delete :
            return False         #업데이트 실행 X

        res=self.create(user_id, new_name)
        return True
        
    @measure_time
    def delete(
        self, 
        user_id: str,
    ) -> bool:  

        read=self.read(user_id)
        if not read : 
            return False 

        table = self.db.Table('Faces')
        res = table.delete_item(
            Key={
                'UserId': user_id
            },
        )
        return True


if __name__ == '__main__':
    enable_measure_time()
    ex=ExternalIdDb()
    ex.delete('11111')
