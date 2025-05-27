from agents.base_agent import BaseAgent
from llm.openai_wrapper import call_gpt
import json
from utils.logger import log

class SeekerAgentWithObstacles(BaseAgent):
    """A seeker agent for navigating grid worlds with obstacles."""
    
    def __init__(self, name, start_position):
        super().__init__(name, start_position)
        # TODO: Initialize seeker agent state
        pass
        
    def decide_move(self, view_data):
        """
        Process the environment view and decide on the next move.
        
        Args:
            view_data (dict): Data about the current environment view
        
        Returns:
            str: Direction to move
        """
        # TODO: Implement decision making logic
        pass 