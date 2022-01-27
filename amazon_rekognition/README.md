# AmazonRekognition

## Set up
- Python `3.10.0`
- pip3 `21.2.4`

```python
pip3 install -r requirements.txt
```

## detect_protecative_equipment
### MaskDetector
```python
mask_detector = MaskDetector(image_path, confidence)
persons = mask_detector.run()
```

result: `List[Person]`
```python
[
    Person(
        bounding_box=BoundingBox(
            height=0.7437499761581421,
            width=0.447857141494751,
            top=0.23839285969734192,
            left=0.0
        ),
        id=0,
        confidence=98.39918518066406,
        body_parts=[
            BodyPart(
                confidence=98.81864929199219,
                equipment_detections=[
                    EquipmentDetection(
                        confidence=99.39614868164062,
                        bounding_box=BoundingBox(
                            height=0.11177883297204971,
                            width=0.11316831409931183,
                            top=0.36089691519737244,
                            left=0.18122929334640503
                        ),
                        covers=CoversBodyPart(
                            confidence=99.62328338623047,
                            value=True
                        ),
                        type='FACE_COVER'
                    )
                ],
                name='FACE'
            ),
            BodyPart(
                confidence=99.38554382324219,
                equipment_detections=[],
                name='HEAD'
            )
        ]
    ),
    Person(
        bounding_box=BoundingBox(
            height=0.7607142925262451,
            width=0.4178571403026581,
            top=0.23839285969734192,
            left=0.5507143139839172
        ),
        id=1,
        confidence=99.63352966308594,
        body_parts=[
            BodyPart(
                confidence=85.94392395019531,
                equipment_detections=[
                    EquipmentDetection(
                        confidence=99.97794342041016,
                        bounding_box=BoundingBox(
                            height=0.13220326602458954,
                            width=0.1318172961473465,
                            top=0.4673272371292114,
                            left=0.6392093896865845
                        ),
                        covers=CoversBodyPart(
                            confidence=94.58857727050781,
                            value=True
                        ),
                        type='FACE_COVER'
                        )
                    ],
                name='FACE'
            ),
            BodyPart(
                confidence=99.99825286865234,
                equipment_detections=[],
                name='HEAD'
            )
        ]
    ),
    Person(
        bounding_box=BoundingBox(
            height=0.6464285850524902,
            width=0.26642856001853943,
            top=0.25357142090797424,
            left=0.3378571569919586
        ),
        id=2,
        confidence=99.74664306640625,
        body_parts=[
            BodyPart(
                confidence=99.2183837890625,
                equipment_detections=[
                    EquipmentDetection(confidence=99.98027801513672,
                    bounding_box=BoundingBox(
                        height=0.0884803906083107,
                        width=0.10158432275056839,
                        top=0.4108157753944397,
                        left=0.40808582305908203
                    ),
                    covers=CoversBodyPart(
                        confidence=94.57086181640625,
                        value=True
                    ),
                    type='FACE_COVER'
                    )
                ],
                name='FACE'
            ),
            BodyPart(
                confidence=99.7402572631836,
                equipment_detections=[],
                name='HEAD'
            )
        ]
    ),
    Person(
        bounding_box=BoundingBox(
            height=0.12857143580913544,
            width=0.09000000357627869,
            top=0.5026785731315613,
            left=0.261428564786911
        ),
        id=3,
        confidence=93.37812805175781,
        body_parts=[
            BodyPart(
                confidence=92.21553802490234,
                equipment_detections=[],
                name='FACE'
            )
        ]
    ),
    Person(
        bounding_box=BoundingBox(
            height=0.14821428060531616,
            width=0.04857143014669418,
            top=0.3821428716182709,
            left=0.5735714435577393
        ),
        id=4,
        confidence=90.71137237548828,
        body_parts=[]
    )
]
```

## search_faces_by_image
### FaceSearcher
```python
face_searcher = FaceSearcher(
    image_path=image_path,
    threshold=threshold,
    max_faces=max_faces,
)

face_matches = face_searcher.run()
```

result: `List[FaceMatch]`
```python
[
    FaceMatch(
        face=Face(
            bounding_box=BoundingBox(
                height=0.3474400043487549,
                width=0.3367069959640503,
                top=0.1785610020160675,
                left=0.3615959882736206
            ),
            confidence=99.99949645996094,
            external_image_id='actor.jpg',
            face_id='50c62b65-33e7-4fa5-ac95-1d8a03cd955a',
            image_id='612cab02-3ee4-308d-bf17-8ed2c88f93a0'
        ),
        similarity=99.99500274658203
    )
]
```