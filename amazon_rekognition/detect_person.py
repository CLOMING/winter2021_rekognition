from typing import Dict, List
import boto3
from utils.measure_time import *
from amazon_rekognition import *

class detect_Person(AmazonRekognition):
    def __init__(   #생성자
        self,
        image: AmazonImage,
    ) -> None:
        self.image = image
        self.client = boto3.client('rekognition')

    def run(self)->T:
        return self.call_rekognition()

    def call_rekognition(self)->T:
        return self.get_response()

    def get_response(self) -> List[Dict]:
        response = self.client.detect_labels(Image={'Bytes': self.image.bytes})
        return self.parse_result(response['Labels'])
    
    def parse_result(self, response: List[Dict]) -> T:
        """
        사람 수 출력
        """
        for label in response:
            if label['Name'] == 'Person':
                return (len(label['Instances']), label) #사람 수 출력
        return None


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pprint import pprint

    parser = ArgumentParser()
    parser.add_argument('--path', required=True)

    args = parser.parse_args()

    image_path = args.path

    detect_person = detect_Person(
        image = AmazonImage.from_file(image_path)
    )
    
    res = detect_person.run()
    
    if res == None:
        print('사람 없음')
    else:
        pprint(res[1])
