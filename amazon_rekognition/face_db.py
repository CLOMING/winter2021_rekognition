import boto3
from decimal import Decimal
from pprint import pprint
from boto3.dynamodb.conditions import Key

#한번 실행한 이후에는 안 씀
def create_Face_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    table = dynamodb.create_table(
        TableName='Faces',
        KeySchema=[
            {
                'AttributeName': 'UserId',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserId',  #Current time 
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

#테이블 삭제라 마찬가지로 안 씀
def delete_Face_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    table = dynamodb.Table('Faces')
    table.delete()


#테이블에 입력 받은 UserId와 Name을 Insert
def put_face(UserId, Name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    table = dynamodb.Table('Faces')
    response = table.put_item(
       Item={
            'UserId': UserId,
            'Name': Name
        }
    )
    return response

#입력 받은 UserId로 일치하는 Name을 검색하여 출력하는 함수
def query_faces(UserId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    table = dynamodb.Table('Faces')
    response = table.query(
        KeyConditionExpression=Key('UserId').eq(UserId)
    )
    return response['Items']



if __name__ == '__main__':

    #Face_table = create_Face_table()  #초기에 한번만 실행 
    #delete_Face_table()                #테이블 지울 때만 실행

    # myUserId = 'a123'
    # myName = '유재석'


    # face_resp = put_face(myUserId, myName)

    query_UserId = 'a123'
    face = query_faces(query_UserId) [0]
    print('UserId: '+face['UserId'] + '\nName: '+face['Name'])
