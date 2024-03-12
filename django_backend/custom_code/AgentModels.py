from global_code.helpful_functions import create_logger_error, log_it, CustomError
import os

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='name',
                             log_to_console=True, log_to_file=False)


class AgentModels:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AgentModels, cls).__new__(cls, *args, **kwargs)
            # Initialize your instance's attributes here
            cls._instance.cheap_llm = "cheap"
            cls._instance.middle_ground_llm = "middle"
            cls._instance.most_intelligent_llm = "top"
            cls._instance.cheap_multimodal_llm = ""
            cls._instance.middle_ground_multimodal_llm = ""
            cls._instance.most_intelligent_multimodal_llm = ""
        return cls._instance

    def set_cheap_llm(self, cheap_llm: str):
        self.cheap_llm = cheap_llm

    def set_middle_ground_llm(self, middle_ground_llm: str):
        self.middle_ground_llm = middle_ground_llm

    def set_most_intelligent_llm(self, most_intelligent_llm: str):
        self.most_intelligent_llm = most_intelligent_llm

    def convert_to_multimodal(self, llm: str) -> str:
        """
        Converts the llm to a multimodal llm
        :param llm: The llm to convert
        :return: The multimodal llm
        """
        if llm == self.cheap_llm:
            return self.cheap_multimodal_llm
        elif llm == self.middle_ground_llm:
            return self.middle_ground_multimodal_llm
        elif llm == self.most_intelligent_llm:
            return self.most_intelligent_multimodal_llm
        else:
            raise CustomError(f"llm {llm} not found")
