from llm.openai_wrapper import call_gpt
from agents.base_navigator import BaseNavigatorAgent
import json
from utils.logger import log

class NavigatorAgentWithoutObstacles(BaseNavigatorAgent):
    def __init__(self, name="Navigator"):
        super().__init__(name)
    
    def getNextPosition(self, current_position, move_direction, environment_data=None):
        """Get the next position based on the move."""
        # TODO: Implement position calculation based on direction
        pass
