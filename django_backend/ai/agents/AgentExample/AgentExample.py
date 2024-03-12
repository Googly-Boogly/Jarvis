from typing import Optional, Literal
import os
from global_code.helpful_functions import create_logger_error, log_it
from custom_code.AgentModels import AgentModels
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='name',
                                 log_to_console=True, log_to_file=False)

"""
To create an entire agent follow these instructions:
1. Copy the example folder in the agent folder IE the example agent
2. Rename the folder to the name of the agent
3. Follow the rest of the documentation, 
4. ENSURE YOU DO NOT CHANGE THE STRUCTURE OF THE AGENT FOLDER, it should have the following:
tools folder, files folder, custom_code folder.
You should first envision what you want the agent too do, than fill out the Agent Class.
Figure out what tools the agent will need, than create the tools.
"""


class AgentExample:
    def __init__(self, past_messages: str, llm: Optional[str] = None, temperature: Optional[float] = None,
                 task_delegation: Optional[bool] = False, emotional_intelligence: Optional[bool] = False,
                 contextual_environmental_memory: Optional[bool] = False):
        """
        To create an agent, follow these instructions:
        1. Rename the class to the name of the agent, ensure the file name is the same as the class name!
        2. Change the default values of llm and temperature
        3. Add tool imports to the top of this file.
        4. Add the tool classes to the tool list in the init function
        5. Decide if the agent needs long-term memory, if so, change the long_term_memory attribute to True
        6. Decide if the agent should be multimodal, if so, change the multimodal attribute to True
        
        :param past_messages: The current state of the conversation is 
        :param llm: The model to use
        :param temperature: The creativity of the agent
        :param task_delegation: If the agent can give its tasks to other agents
        :param emotional_intelligence: If the agent has emotional intelligence
        :param contextual_environmental_memory: If the agent has access to specialized information about the environment
        """
        stuff = self.change_these_attributes()
        self.agent_name = stuff['agent_name']
        self.agent_description = stuff['agent_description']
        self.base_temp = stuff['base_temp']
        self.base_model = stuff['base_model']
        self.tools = stuff['tools']

        self.long_term_memory = stuff['long_term_memory']
        # Multimodal (This is if the agent should have access to vision and hearing)
        self.multimodal = stuff['multimodal']
        
        # Future attributes (STILL WORK IN PROGRESS DON'T TURN THEM ON YET)
        self.contextual_environmental_memory = stuff['contextual_environmental_memory']
        self.task_delegation = stuff['task_delegation']
        self.emotional_intelligence = stuff['emotional_intelligence']

        # Needed logic
        if self.multimodal:
            self.llm = AgentModels().convert_to_multimodal(self.llm)
        self.past_messages = past_messages
        if llm:
            self.llm = llm
        if temperature:
            self.temperature = temperature
        if task_delegation:
            self.task_delegation = True
        if emotional_intelligence:
            self.emotional_intelligence = True
        if contextual_environmental_memory:
            self.contextual_environmental_memory = True

    @staticmethod
    def change_these_attributes() -> dict:
        """
        This function is used to change the attributes of the agent
        :return: The attributes of the agent including the name, description, temperature, model, and tools
        """
        # TODO CHANGE THESE TO CREATE AN AGENT
        agent_description = """

"""
        # NEEDS TO BE THE SAME AS THE CLASS NAME
        agent_name = "AgentExample"

        # Model has 3 options for llm; AgentModels().cheap_llm, AgentModels().middle_ground_llm,
        # AgentModels().most_intelligent_llm
        llm = AgentModels().cheap_llm

        # The temperature is a float between 0 and 1
        # .9 is most creative and least factual, 0.1 is least creative and most factual
        temperature = 0.1

        if temperature not in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            raise CustomError("Temperature must be a float between 0 and 1")

        # Should be strings of the EXACT tool names.
        tools = ["ToolExample"]

        # WIP
        long_term_memory = False
        task_delegation = False
        emotional_intelligence = False  # Lol
        contextual_environmental_memory = False

        output = {
            "agent_name": agent_name,
            "agent_description": agent_description,
            "base_temp": temperature,
            "base_model": llm,
            "tools": tools,
            "long_term_memory": long_term_memory,
            "multimodal": multimodal,
            "task_delegation": task_delegation,
            "emotional_intelligence": emotional_intelligence,
            "contextual_environmental_memory": contextual_environmental_memory
        }

        return output



