import json
import requests
import os
from global_code.singleton import State
from global_code.helpful_functions import create_logger_error, log_it
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='name',
                                 log_to_console=True, log_to_file=False)


def create_mp3_file(text: str):
    """Creates an mp3 file from the given text"""

    url = "https://api.edenai.run/v2/audio/text_to_speech"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "rate": 0,
        "pitch": 0,
        "volume": 0,
        "settings": '{"amazon": "en-US_Kimberly_Neural"}',
        "sampling_rate": 0,
        "providers": "amazon",
        "text": "Hello My name is Jarvis"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {State.config['EDEN_AI_API_KEY']}",
    }

    response = requests.post(url, json=json.dumps(payload), headers=headers)

    log_it(logger, error=None, custom_message=f'{response}')