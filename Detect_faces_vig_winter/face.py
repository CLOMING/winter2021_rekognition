import boto3
from botocore.exceptions import ClientError
from pprint import pprint

def add_faces_to_collection(bucket,photo,collection_id):
    
    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def describe_collection(collection_id):

    print('Attempting to describe collection ' + collection_id)
    client=boto3.client('rekognition')

    try:
        response=client.describe_collection(CollectionId=collection_id)
        print("Collection Arn: "  + response['CollectionARN'])
        print("Face Count: "  + str(response['FaceCount']))
        print("Face Model Version: "  + response['FaceModelVersion'])
        print("Timestamp: "  + str(response['CreationTimestamp']))

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
    print('Done...')



def compare_faces(sourceName, targetFile, bucket):

    client=boto3.client('rekognition')
   
  # imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'S3Object': {'Bucket':bucket,'Name':sourceName}},
                                  TargetImage={'Bytes': imageTarget.read()})
    pprint(response)

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + similarity + '% confidence')

    imageTarget.close()     
    return len(response['FaceMatches'])    



if __name__=="__main__":
    bucket='vigwinter'
    target_file='/home/hsj/Documents/vig/winter2021_recognition/Detect_faces_vig_winter/dujun.jpg'
    target_file='/home/hsj/Documents/vig/winter2021_recognition/Detect_faces_vig_winter/joohyuk.jpg'
    source_name='dujun1.jpg'
    fileName=''

    client=boto3.client('rekognition')
    collection_id='face_collection'
    
    # # collection 생성 (face_collection)
    # response1=client.create_collection(CollectionId=collection_id)
    # print('CollectionARN:'+response1['CollectionArn'])

    # collection에 얼굴추가
    # indexed_faces_count=add_faces_to_collection(bucket, photo, collection_id)
    # print("Faces indexed count: " + str(indexed_faces_count))

    # collection describe
   # describe_collection(collection_id)

    # 얼굴 비교
    face_matches=compare_faces(source_name, target_file,bucket)
    print("Face matches: " + str(face_matches))