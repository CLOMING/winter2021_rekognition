"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).

class TTS():
    
    def __init__(
        self,
        text:str,
    ) -> None:
        self.text=text
        session = Session(profile_name="soojin_polly")
        self.polly = session.client("polly")

    def get_response(self)->None:
        try:
            response=self.polly.synthesize_speech(Text=self.text, OutputFormat="mp3",
                                                VoiceId="Seoyeon")
            #print(response)
        except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3") # path 
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)
        else:
            print("Could not stream audio")
            sys.exit(-1)

        if sys.platform == "win32":
            os.startfile(output)
        
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])


