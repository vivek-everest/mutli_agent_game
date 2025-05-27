from agents.base_agent import BaseAgent
from llm.openai_wrapper import call_gpt
import json
from utils.logger import log

class SeekerAgentWithoutObstacles(BaseAgent):
    def __init__(self, name, start_position):
        super().__init__(name, start_position)

    def decide_move(self, view_data):
        """
        Decide the next move based on clues and exploration.
        
        Args:
            view_data (dict): Data about the current environment view
            
        Returns:
            str: Direction to move
        """
        # TODO: Implement the seeker's decision logic
        pass