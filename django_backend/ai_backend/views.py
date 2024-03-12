from typing import List, Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
import os
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from global_code.helpful_functions import create_logger_error, log_it
from db.tables.users import User
from db.tables.total_chats import TotalChats
from db.tables.website_state import WebsiteState
from db.tables.Message import Message
from db.tables.chats import Chat
from db.tables.models import Model
from db.tables.agents import Agent
from ai.other.text_to_speech import create_mp3_file, read_speech_file, delete_speech_file
from custom_code.user_sent_message import user_sent_message
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='name',
                                 log_to_console=True, log_to_file=False)


class WhisperModelAPI(APIView):
    def get(self, request, format=None):
        # Placeholder for your GET request logic
        return Response({"message": "This is a GET request"})

    def post(self, request, format=None):
        # Placeholder for handling POST request, e.g., streaming audio data
        return Response({"message": "This is a POST request"})


class STTOnOffBtn(APIView):
    def post(self, request, *args, **kwargs):
        stt_on_off = request.data.get('stt_on_off')
        # log_it(logger, error=None, custom_message=f'{request.data}')

        if not stt_on_off:
            stt_on_off = 0
        else:
            stt_on_off = 1
        WebsiteState({}).edit_any_row(new_name=stt_on_off, primary_key=1, row_name='stt')
        return Response({"SUCCESS": "200"})


class TtsOnOff(APIView):
    def post(self, request, *args, **kwargs):
        tts_on_off = request.data.get('tts_on_off')
        # log_it(logger, error=None, custom_message=f'{request.data}')

        if not tts_on_off:
            tts_on_off = 0
        else:
            tts_on_off = 1
        WebsiteState({}).edit_any_row(new_name=tts_on_off, primary_key=1, row_name='tts')
        return Response({"SUCCESS": "200"})




class ModelSelector(APIView):
    """Changes the selected model"""
    def post(self, request, *args, **kwargs):

        model_name = request.data.get('value')
        if not model_name:
            return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        WebsiteState({}).edit_any_row(new_name=model_name, primary_key=1, row_name='model_selected')
        return Response({"SUCCESS": "200"})


class TemperatureSelector(APIView):
    """Changes the selected temperature"""
    def post(self, request, *args, **kwargs):

        temperature = request.data.get('value')
        if not temperature:
            return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        WebsiteState({}).edit_any_row(new_name=temperature, primary_key=1, row_name='temperature')
        return Response({"SUCCESS": "200"})


class AgentSelected(APIView):
    """Changes the selected agent"""
    def post(self, request, *args, **kwargs):

        agent_selected = request.data.get('value')
        if not agent_selected:
            return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        # model_id = Model({}).select_one_for_name(name=model_name)[0]['model_id']
        WebsiteState({}).edit_any_row(new_name=agent_selected, primary_key=1, row_name='agent_selected')

        return Response({"SUCCESS": "200"})


class ChatSelection(APIView):
    """Changes the selected chat"""
    def post(self, request, *args, **kwargs):
        log_it(logger, error=None, custom_message=f'Chat Change Request: {request.data}')
        chat_id = request.data.get('chat_id')
        if not chat_id:
            return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        WebsiteState({}).edit_any_row(new_name=chat_id, primary_key=1, row_name='current_chat')
        return Response({'SUCCESS': '200'})


class CreateNewChat(APIView):
    """Changes the selected chat"""
    def post(self, request, *args, **kwargs):
        # create_new_chat = request.data.get('create_new_chat')
        # if not create_new_chat:
        #     return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        new_chat_id = Chat({"title": "New Chat", "total_chats_id": 1}).save()
        WebsiteState({}).edit_any_row(new_name=new_chat_id, primary_key=1, row_name='current_chat')
        return Response({'SUCCESS': '200'})


class ServeMp3(APIView):
    """Serves the speech.mp3 file."""

    def get(self, request, *args, **kwargs):
        return self.serve_file()

    def post(self, request, *args, **kwargs):
        return self.serve_file()

    def serve_file(self):
        file_path = r"/src/media/speech.mp3"
        file_name = "speech.mp3"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                mp3_data = f.read()
            response = HttpResponse(mp3_data, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
        else:
            return HttpResponse(status=404)



class UserSendsMessage(APIView):
    """Changes the selected chat"""
    def post(self, request, *args, **kwargs):
        create_new_chat = request.data.get('create_new_message')
        if not create_new_chat:
            return Response({'error': 'Model ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        web_state: dict = WebsiteState({}).select_one_for_primary(1)[0]
        # log_it(logger, error=None, custom_message=f'Website State: {web_state}')
        Message({'model': "User", 'agent': "User",
                 'temp': 0.0,
                 'chat_id': web_state['current_chat'], 'message': create_new_chat}).save()
        total_chat = Chat({}).select_one_for_primary(web_state['current_chat'])[0]
        # log_it(logger, error=None, custom_message=f'total_chat: {total_chat}')
        # log_it(logger, error=None, custom_message=f'all_msg: {Message({}).select_all()}')
        # total_chat: dict = TotalChats({}).select_one_for_primary(web_state['current_chat'])[0]
        ai_response: str = user_sent_message(total_chat, web_state)
        Message({'model': web_state["model_selected"], 'agent': web_state["agent_selected"],
                 'temp': web_state["temperature"],
                 'chat_id': web_state['current_chat'], 'message': ai_response}).save()
        current_chat_frontend_version: List[Dict[str, str]] = []
        current_chat_db_version = Message({}).select_one_where_chat_id(web_state['current_chat'])

        for chat in current_chat_db_version:
            if chat['model'] == 'User':
                current_chat_frontend_version.append({"who_said_it": "User", "text": chat['message']})
            else:
                current_chat_frontend_version.append({"who_said_it": "Jarvis", "text": chat['message']})

        if web_state['tts'] == 0:
            log_it(logger, error=None, custom_message=f'STT AI: {ai_response}')
            create_mp3_file(ai_response)
            speech_file = read_speech_file()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'audio_group',  # Use the same group name as in your consumer
                {
                    'type': 'audiomessage',  # Matches the method in the consumer
                    'message': speech_file
                }
            )

        return Response(current_chat_frontend_version)


class GetWebsiteState(APIView):
    """Changes the selected chat"""
    def get(self, request, *args, **kwargs):

        web_state: dict = WebsiteState({}).select_one_for_primary(1)[0]
        log_it(logger, error=None, custom_message=f'Website State: {web_state}')
        current_chat_frontend_version: List[Dict[str, str]] = [] # Only things in the dict will be who_said_it and text
        current_chat_db_version = Message({}).select_one_where_chat_id(web_state['current_chat'])

        for chat in current_chat_db_version:
            if chat['model'] == 'User':
                current_chat_frontend_version.append({"who_said_it": "User", "text": chat['message']})
            else:
                current_chat_frontend_version.append({"who_said_it": "Jarvis", "text": chat['message']})
        past_convos_db_version = Chat({}).select_all()
        past_convos_frontend_version = []
        # Make the same loop but loop through in opposite order
        for chat in reversed(past_convos_db_version):
            past_convos_frontend_version.append(chat)

        web_state["past_convos"] = past_convos_frontend_version
        web_state["current_convo"] = current_chat_frontend_version
        web_state["agents"] = Agent({}).select_all()
        web_state["models"] = Model({}).select_all()

        return Response(web_state)



