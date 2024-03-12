import os
from tests.test_function_json import unit_test_validate_function
from global_code.helpful_functions import create_logger_error, log_it
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='tool',
                                 log_to_console=True, log_to_file=False)


class ToolExample:
    # TODO change the inputs to the tool
    def __init__(self, input_to_tool: str):
        """
        This class is an example of a tool class, a tool is as simple as a function that takes an input and returns an output
        It can be anything, creating a calendar event, getting the weather, calling an api, doing something with a database, etc.
        It should be something that interacts with the outside world.
        
        To create a tool, follow these instructions:
        1. Rename the class to the name of the tool, ensure the file name is the same as the class name!
        2. Fill in the inputs for this init function. 
        3. Fill out the json representation of this tool in the json_of_tool function the name is the same as the file name!
        (if you get an error, it's not the unit test, it's your json)
        4. Now actually create the code to get the tool to work.
        5. Change the function in the tool function of this class.
        
        That's it!
        You have created a tool!
        :param input_to_tool: Example input
        """
        self.input_to_tool = input_to_tool

        # Ensure you always create these attributes
        self.json_representation = self.json_of_tool()
        self.name = self.json_representation['name']
        self.description = self.json_representation['description']
        self.inputs = self.json_representation['parameters']['properties']

    def run(self) -> str:
        """
        This is the function that will be called when the tool is used
        :return: The outcome of the tool,
        Could be an error or the output of the tool, or the wrong output of the tool
        """
        output = ''
        try:
            # TODO Put your function here
            output: str = do_the_function(self.input_to_tool)
        except Exception as e:
            log_it(logger, error=e, custom_message=f'Error in tool {self.name}: {e}')
            output = f"Error in {self.name}: {e}"
        finally:
            assert isinstance(output, str)
            return output
    
    @staticmethod
    def json_of_tool() -> dict:
        """
        Returns the json representation of the tool
        :return: The json representation of the tool
        """
        # This is an example of a json representation of a tool that creates a calendar event
        # TODO Change this than delete this comment when done
        json_of_tool = {
            "name": 'ToolExample',
            "description": 'create a calendar event',
            "parameters": {
                "type": 'object',
                'properties': {
                    "start_time": {
                        'type': 'string',
                        'description': 'datetime of the start of the event',
                    },
                    'end_time': {
                        'type': 'string',
                        'description': 'datetime of the end of the event',
                    },
                    'summary': {
                        'type': 'string',
                        'description': 'title of the event',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'description of the event including any details that are known',
                    }
                },
                'required': ['start_time', 'end_time', 'summary']
            },

        }
        unit_test_validate_function(json_of_tool)
        return json_of_tool


def do_the_function(input_to_tool: str) -> str:
    pass

