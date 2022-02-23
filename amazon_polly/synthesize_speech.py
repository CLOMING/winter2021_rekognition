from contextlib import closing
import io
from typing import Any, Optional

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from pydub import AudioSegment
from pydub.playback import play


class TTS():

    def __init__(self, ) -> None:
        session = Session(profile_name="default")
        self.polly = session.client("polly")

    def read(self, text: str) -> None:
        try:
            response = self.polly.synthesize_speech(Text=text,
                                                    OutputFormat="mp3",
                                                    VoiceId="Seoyeon")
        except (BotoCoreError, ClientError) as error:
            raise TTSException('Boto Error occured.', error)

        if not "AudioStream" in response:
            raise TTSAudioStreamNotExistException()

        with closing(response['AudioStream']) as stream:
            audio_data = stream.read()

        sound = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        play(sound)


class TTSException(Exception):

    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.data = data

    def __str__(self) -> str:
        error_message: str = f'[TTSException] {self.message}'

        if self.data:
            error_message += f'\n{self.data}'

        return error_message


class TTSAudioStreamNotExistException(TTSException):

    def __init__(self) -> None:
        super().__init__('AudioStream is not exist.')
