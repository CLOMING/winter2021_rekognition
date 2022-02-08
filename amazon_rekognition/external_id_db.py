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
        """
        Table을 생성.\n
        face_db.py에 있는 create_Face_table 함수를 사용.\n     
        Table의 이름은 임의로 정하지 않고, Faces로 하였음.
        """
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
        """
        Table을 삭제\n
        face_db.py에 있는 delete_Face_table 함수를 사용.\n
        삭제할 Table의 이름은 임의로 정하지 않고, Faces로 고정.
        """
        table = self.db.Table('Faces')
        table.delete()

    def create(
        self,
        user_id: str,
        name: str,
    ):
        """
        입력한 User id와 Name을 Faces Table에 추가
        """
        read = self.read(user_id)
        if read != None:
            return None  #ㅣ미 있는 것
    
        table = self.db.Table('Faces')
        res = table.put_item(
            Item = {
                'UserId': user_id,
                'UserName': name
            }
        )
        return True
        # TODO: put_item의 결과를 Dataclass 형태로 담아서 return
        #pass
    
    @measure_time
    def read(
        self,
        user_id: str,
    ):
        """
        user id로 name을 검색해서, name을 리턴
        """
        table = self.db.Table('Faces')
        res = table.get_item(
            Key={
                'UserId': user_id
            }
        )
        if 'Item' in res:
            return res['Item']['UserName']
        else:
            return None

        # TODO: Table에서 user_id로 검색한 결과를 반환
        # TODO: 검색해 찾은 name을 return, 검색한 결과가 없다면 None return
        #pass

    def update(
        self,
        user_id: str,
        new_name: str,
    ):
        """
        입력한 User id를 갖는 Name을 new name으로 변경\n
        만약 입력한 user id가 없어도 자동으로 등록되는 문제 발생
        """
        delete = self.delete(user_id)
        if delete == None:
            return None         #업데이트 실행 X

        res=self.create(user_id, new_name)
        return True
        # TODO: user_id의 name을 new_name으로 변경
        # TODO: 결과를 dataclass로 wrapping 해서 반환
        
    @measure_time
    def delete(
        self, 
        user_id: str,
    ):  
        """
        입력한 User id를 갖는 데이터를 Table에서 삭제\n
        없는 User id를 입력했을 때를 확인하기 위해 read를 먼저 확인해야 됨.\n
        단순히 delete_item에서는 판단할 수 있는 기능이 없음
        """
        read=self.read(user_id)
        if read == None:
            return None
        else:  
            table = self.db.Table('Faces')
            res = table.delete_item(
                Key={
                    'UserId': user_id
                },
            )
            return True
'''
{'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                      'content-length': '2',
                                      'content-type': 'application/x-amz-json-1.0',
                                      'date': 'Tue, 08 Feb 2022 05:10:50 GMT',
                                      'server': 'Server',
                                      'x-amz-crc32': '2745614147',
                                      'x-amzn-requestid': 'OVN3MDV9B7K9NNTMB310QNTBONVV4KQNSO5AEMVJF66Q9ASUAAJG'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'OVN3MDV9B7K9NNTMB310QNTBONVV4KQNSO5AEMVJF66Q9ASUAAJG',
                      'RetryAttempts': 0}}

                      이런 형태로 결과가 출력됨. create도 마찬가지
'''

        # TODO: Table에서 user_id를 삭제
        # TODO: 결과를 datacalss를 사용해서 wrapping 해서 return

    

if __name__ == '__main__':
    enable_measure_time()
    ex=ExternalIdDb()
    ex.delete('9')
