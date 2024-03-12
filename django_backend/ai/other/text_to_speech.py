from global_code.singleton import State
from pathlib import Path
import os
from global_code.helpful_functions import create_logger_error, log_it, CustomError
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='tool',
                                 log_to_console=True, log_to_file=False)


def create_mp3_file(text: str) -> str:
    """
    This function is used to convert text to speech.
    :param text: The text to convert to speech
    :return: The file path of the audio file
    """
    log_it(logger, error=None, custom_message=f"Text to speech: {text}")
    speech_file_path = r"/src/media/speech.mp3"
    if os.path.exists(speech_file_path):
        os.remove(speech_file_path)
    # Get the state
    client = State.client
    # Get the agent
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input=text
    )

    response.stream_to_file(speech_file_path)
    log_it(logger, error=None, custom_message=f"Text to speech: {text}")
    return str(speech_file_path)


def delete_speech_file():
    """
    This function is used to delete the speech file
    """
    speech_file_path = Path(__file__).parent / "speech.mp3"
    if speech_file_path.exists():
        speech_file_path.unlink()


def read_speech_file() -> bytes:
    """
    This function is used to read the speech file
    :return: The speech file
    """
    speech_file_path = r"/src/media/speech.mp3"

    with open(speech_file_path, 'rb') as fh:
        file = fh.read()
        return file
    # else:
    #     raise CustomError("The file does not exist")