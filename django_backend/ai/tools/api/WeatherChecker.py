import os
from tests.test_function_json import unit_test_validate_function
from global_code.helpful_functions import create_logger_error, log_it
from custom_code.check_weather import check_weather
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='tool',
                                 log_to_console=True, log_to_file=False)


class WeatherChecker:
    def __init__(self, city: str):
        """
        This class is an example of a tool class, a tool is as simple as a function that takes an input and returns an output
        It can be anything, creating a calendar event, getting the weather, calling an api, doing something with a database, etc.
        It should be something that interacts with the outside world.
        
        To create a tool, follow these instructions:
        1. Rename the class to the name of the tool, ensure the file name is the same as the class name!
        2. Fill in the inputs for this init function. 
        3. Fill out the json representation of this tool in the json_of_tool function
        (if you get an error, it's not the unit test, it's your json)
        4. Now actually create the code to get the tool to work.
        5. Add any imports to the top of this file.
        6. Change the function in the tool function of this class.
        
        That's it!
        You have created a tool!
        :param input_to_tool: Example input
        """
        self.city = city

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
            # Put your function here
            output: str = check_weather(self.city)
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
        json_of_tool = {
            "name": 'WeatherChecker',
            "description": 'Will check the current weather in a city',
            "parameters": {
                "type": 'object',
                'properties': {
                    "city": {
                        'type': 'string',
                        'description': 'The city to check the weather in',
                    },
                },
                'required': ['city']
            },

        }
        unit_test_validate_function(json_of_tool)
        return json_of_tool

