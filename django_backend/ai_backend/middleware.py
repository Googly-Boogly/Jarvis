# myapp/middleware.py
import os
import importlib.util
import sys

from db.tables.agents import Agent
from db.tables.Functions import Function
from global_code.helpful_functions import create_logger_error, log_it
from db.tables.AgentFunctions import AgentFunctions
from db.tables.users import User
from db.tables.total_chats import TotalChats
from db.tables.website_state import WebsiteState
from db.tables.Message import Message
from db.tables.chats import Chat
from db.tables.models import Model
from db.tables.agents import Agent
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='middleware',
                                 log_to_console=True, log_to_file=False)


class RunOnceMiddleware:
    has_run = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.__class__.has_run:
            self.run_once()
            self.__class__.has_run = True
        return self.get_response(request)

    @staticmethod
    def run_once():
        # Your initialization code here
        log_it(logger, error=None, custom_message="Running initialization code")
        check_user()
        tools_dir = r"ai/tools"
        find_and_register_tools(tools_dir)
        target_directory = 'ai/agents'  # Set the path to your target directory
        load_and_register_agents(target_directory)

        # for folder_name in os.listdir(target_directory):
        #     folder_path = os.path.join(target_directory, folder_name)
        #     if os.path.isdir(folder_path):
        #         Folder.objects.get_or_create(name=folder_name)



        all_functs = Function({}).select_all()
        log_it(logger, error=None, custom_message=f"ALL FUNCTS: {all_functs}")
        all_agents = Agent({}).select_all()
        log_it(logger, error=None, custom_message=f"ALL AGENTS: {all_agents}")
        all_agent_functions = AgentFunctions().select_all()
        log_it(logger, error=None, custom_message=f"ALL AGENT FUNCTIONS: {all_agent_functions}")


def load_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_and_register_tools(tools_dir):
    """
    Will search the tools directory for any tools and register them in the database
    :param tools_dir:
    :return:
    """
    for root, dirs, files in os.walk(tools_dir):
        for file in files:
            if file == '__init__.py' or file == "ToolExample.py":
                continue
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module = load_module_from_file(file_path)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type):  # Check if the attribute is a class
                        if hasattr(attr, 'json_of_tool'):
                            tool_info = attr.json_of_tool()
                            if not Function({}).select_one_for_name(tool_info['name']):
                                Function({
                                    "function_name": tool_info['name'],
                                    "function_description": tool_info['description'],
                                    "function_inputs": tool_info['parameters']['properties'],
                                    "function_output": "",
                                    "function_json": tool_info
                                }).save()
                                log_it(logger, error=None, custom_message=f"Registered tool: {tool_info['name']}")


def load_and_register_agents(target_directory):
    """
    Will search the target directory for any agents and register them in the database
    :param target_directory:
    :return:
    """
    for agent_name in os.listdir(target_directory):
        if agent_name == '__pycache__' or agent_name == "AgentExample":
            continue
        agent_dir_path = os.path.join(target_directory, agent_name)
        if os.path.isdir(agent_dir_path):
            agent_file_path = os.path.join(agent_dir_path, f"{agent_name}.py")
            if os.path.isfile(agent_file_path):
                module = load_module_from_file(agent_file_path)
                if hasattr(module, agent_name):
                    agent_class = getattr(module, agent_name)
                    if hasattr(agent_class, 'change_these_attributes'):
                        attributes = agent_class.change_these_attributes()
                        # Check if the agent is already in the DB
                        agent_id_check = Agent({}).select_one_for_name(agent_name)

                        if not agent_id_check:
                            # If it is, update the attributes
                            agent_id = Agent({
                                "agent_name": agent_name,
                                "agent_description": attributes['agent_description'],
                                "base_temp": attributes['base_temp'],
                                "base_model": attributes['base_model'],
                                "long_term_memory": attributes['long_term_memory'],
                                "contextual_environmental_memory": attributes['contextual_environmental_memory'],
                                "task_delegation": attributes['task_delegation'],
                                "emotional_intelligence": attributes['emotional_intelligence']
                            }).save()
                            tools_li = attributes['tools']
                            for tool in tools_li:
                                function_id = Function({}).select_one_for_name(tool)[0]['function_id']
                                # log_it(logger, error=None, custom_message=f"Function ID: {function_id}")
                                # log_it(logger, error=None, custom_message=f"Agent ID: {agent_id}")
                                AgentFunctions().link_agent_to_function(agent_id=agent_id, function_id=function_id)
                            log_it(logger, error=None,
                                   custom_message=f"Registered agent: {agent_name}")


def check_user():
    """
    Checks if DB is already populated if not will populate it
    :return:
    """
    if not User({}).select_one_for_primary(1):
        TotalChats({
            'total_chats_id': 0,
            'total_chats': 0
        }).save()
        User({
            'password': 'password',
            'name': 'admin',
            'total_chats_id': 1
        }).save()
        Chat({"title": "Theory of the universe", "total_chats_id": 1}).save()
        Chat({"title": "Testing something", "total_chats_id": 1}).save()
        WebsiteState({
            'website_state_id': 0,
            'user_id': 1,
            'tts': 0,
            'stt': 0,
            'current_chat': 1,
            'model_selected': 'Gpt 3.5',
            'temperature': 0.7,
            'agent_selected': 'none'
        }).save()
        Model({"model_name": "Auto", "model_info": "Let the gods decide your fate", "company": "NA"}).save()
        Model({"model_name": "Gpt 3.5", "model_info": "16k context window", "company": "OpenAI"}).save()
        Model({"model_name": "Gpt 4", "model_info": "128k context window", "company": "OpenAI"}).save()
        Model({"model_name": "Gpt 4V", "model_info": "128k context window, multimodal", "company": "OpenAI"}).save()
        Model({"model_name": "Gemini Pro", "model_info": "128k context window, multimodal", "company": "Google"}).save()
        Model({"model_name": "Gemini 1.5", "model_info": "1M context window, multimodal", "company": "Google"}).save()
        Model({"model_name": "Mixtral 8x7b", "model_info": "32k context window", "company": "Mistral"}).save()
        Model({"model_name": "Mistral 7b", "model_info": "32k context window", "company": "Mistral"}).save()
        Model({"model_name": "Claude 3 Haiku", "model_info": "200k context window, multimodal, cheapest", "company": "Anthropic"}).save()
        Model({"model_name": "Claude 3 Sonnet", "model_info": "200k context window, multimodal, middle-ground", "company": "Anthropic"}).save()
        Model({"model_name": "Claude 3 Opus", "model_info": "200k context window, multimodal, best & pricey", "company": "Anthropic"}).save()

        Agent({"agent_name": "None", "agent_description": "No agent selected", "base_temp": 0.1, "base_model": "Gpt 3.5",
               "long_term_memory": False,
               "contextual_environmental_memory": False,
               "task_delegation": False,
               "emotional_intelligence": False
               }).save()
        Agent({"agent_name": "Everything", "agent_description": "All agents combined", "base_temp": 0.1, "base_model": "Gpt 3.5",
               "long_term_memory": True,
               "contextual_environmental_memory": True,
               "task_delegation": False,
               "emotional_intelligence": False
               }).save()

        log_it(logger, error=None, custom_message='User and TotalChats, Website_state, models, chats tables have been initialized.')
