#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor


def show_faces(photo):
    image = Image.open(photo)
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected face
    print('Detected faces for ' + photo)
    faceDetail = response['FaceMatches']['Face']
    #for faceDetail in response['FaceMatches']:
    box = faceDetail['BoundingBox']
    left = imgWidth * box['Left']
    top = imgHeight * box['Top']
    width = imgWidth * box['Width']
    height = imgHeight * box['Height']

    print('Left: ' + '{0:.0f}'.format(left))
    print('Top: ' + '{0:.0f}'.format(top))
    print('Face Width: ' + "{0:.0f}".format(width))
    print('Face Height: ' + "{0:.0f}".format(height))

    points = ((left, top), (left + width, top), (left + width, top + height),
              (left, top + height), (left, top))
    draw.line(points, fill='#00d400', width=2)

    # Alternatively can draw rectangle. However you can't set line width.
    #draw.rectangle([left,top, left + width, top + height], outline='#00d400')

    image.show()


if __name__ == "__main__":

    collectionId = 'User_Collection'
    fileName = 'winter2021_recognition/Detect_faces_vig_winter/joohyuk.jpg'
    threshold = 70
    maxFaces = 2

    client = boto3.client('rekognition')

    imageTarget = open(fileName, 'rb')
    response = client.search_faces_by_image(
        CollectionId=collectionId,
        # Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
        Image={'Bytes': imageTarget.read()},
        FaceMatchThreshold=threshold,
        MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']
    print('Matching faces')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
    show_faces(fileName)
