#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
import boto3
import io
import os
from PIL import Image, ImageDraw, ExifTags, ImageColor
from pprint import pprint

def detect_labels(photo, confidence):
    fill_green='#00d400'
    fill_red='#ff0000'
    fill_yellow='#ffff00'
    line_width=3

    #open image and get image data from stream.
    image = Image.open(open(photo,'rb'))
    stream = io.BytesIO()
    image.save(stream, format=image.format)    
    image_binary = stream.getvalue()
    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)  

    client=boto3.client('rekognition')

    response = client.detect_protective_equipment(Image={'Bytes': image_binary},
        SummarizationAttributes={'MinConfidence':80, 'RequiredEquipmentTypes':['FACE_COVER']})
 
    #pprint(response)



    for person in response['Persons']:
        found_mask=False
        for body_part in person['BodyParts']:
            ppe_items = body_part['EquipmentDetections']
                 
            for ppe_item in ppe_items:
                #found a mask 
                if ppe_item['Type'] == 'FACE_COVER':
                    fill_color=fill_green
                    found_mask=True
                    # check if mask covers face
                    if ppe_item['CoversBodyPart']['Value'] == False:
                        fill_color=fill='#ff0000'
                    # draw bounding box around mask
                    box = ppe_item['BoundingBox']
                    left = imgWidth * box['Left']
                    top = imgHeight * box['Top']
                    width = imgWidth * box['Width']
                    height = imgHeight * box['Height']
                    points = (
                            (left,top),
                            (left + width, top),
                            (left + width, top + height),
                            (left , top + height),
                            (left, top)
                        )
                    draw.line(points, fill=fill_color, width=line_width)

                     # Check if confidence is lower than supplied value       
                    if ppe_item['CoversBodyPart']['Confidence'] < confidence:
                        #draw warning yellow bounding box within face mask bounding box
                        offset=line_width+ line_width 
                        points = (
                                    (left+offset,top + offset),
                                    (left + width-offset, top+offset),
                                    ((left) + (width-offset), (top-offset) + (height)),
                                    (left+ offset , (top) + (height -offset)),
                                    (left + offset, top + offset)
                                )
                        draw.line(points, fill=fill_yellow, width=line_width)
                
        if found_mask==False:
            # no face mask found so draw red bounding box around body
            box = person['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']
            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top)
                )
            draw.line(points, fill=fill_red, width=line_width)
        
        print('Person ID: ' + str(person['Id'])+'\n---------------\n')
        body_parts = person['BodyParts']
        if len(body_parts) == 0:
            print ('No body parts found')

        else:       
            if not body_parts[0]['EquipmentDetections']:
                print('\tPersion ID: '+str(person['Id'])+' ->마스크 미착용')
            else:
                if body_parts[0]['EquipmentDetections'][0]['CoversBodyPart']['Value']:
                    print('\tPersion ID: '+str(person['Id'])+' ->마스크 착용')
                else:
                    print('\tPersion ID: '+str(person['Id'])+' ->마스크 미착용')
        print()
    print('---------------')
    image.show()
    return len(response['Persons'])  #인원 수 출력

def main():
    photo='image/test_1.jpg' 
    #mask1.jpg
    #mask2.jpg
    #ppe0.jpg
    #ppe1.jpg
    #ppe2.jpg
    #HI
    bucket='vigwinter'
    confidence=80  #신뢰도

    person_count=detect_labels(photo, confidence)
    print("Persons detected: " + str(person_count))

if __name__ == "__main__":
    main()


#this is modification