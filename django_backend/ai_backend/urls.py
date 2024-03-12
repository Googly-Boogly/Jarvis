"""ai_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (UserSendsMessage, GetWebsiteState, TtsOnOff, WhisperModelAPI, STTOnOffBtn,
                    ModelSelector, TemperatureSelector, AgentSelected, ChatSelection, CreateNewChat,
                    ServeMp3)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/whisper', WhisperModelAPI.as_view(), name='whisper_api'),
    path('api/stt_toggle', STTOnOffBtn.as_view(), name='stt_toggle'),
    path('api/tts_toggle', TtsOnOff.as_view(), name='tts_toggle'),
    path('api/model_change', ModelSelector.as_view(), name='model_change'),
    path('api/temp_change', TemperatureSelector.as_view(), name='temp_change'),
    path('api/agent_select', AgentSelected.as_view(), name='agent_select'),
    path('api/chat_select', ChatSelection.as_view(), name='chat_select'),
    path('api/create_new_chat', CreateNewChat.as_view(), name='create_new_chat'),
    path('api/send_message', UserSendsMessage.as_view(), name='send_message'),
    path('api/get_web_state', GetWebsiteState.as_view(), name='get_web_state'),
    path('api/serve_mp3', ServeMp3.as_view(), name='serve_mp3'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
