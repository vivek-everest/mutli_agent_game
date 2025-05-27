from llm.openai_wrapper import call_gpt
from agents.base_navigator import BaseNavigatorAgent
import json
from utils.logger import log

class NavigatorAgentWithObstacles(BaseNavigatorAgent):
    def __init__(self, name="Navigator"):
        super().__init__(name)
    
    def getNextPosition(self, current_position, move_direction, environment_data=None):
        """Get the next position based on the move."""
        self.visited_positions.add(tuple(current_position))
        
        if environment_data and 'visible_obstacles' in environment_data:
            self.update_environment_data(environment_data)
        
        prompt = (
            f"You are a navigator agent in a grid world of 10x10 with obstacles and you are in a treasure hunt game.\n"
            f"The treasure will be hidden in one of the 10x10 cells.\n"
            f"Your task is to calculate the exact next position based on the current position and move direction while avoiding obstacles.\n"
            f"Each time you will get the current position, and the suggested move by a seeker agent.\n"
            f"You have to find the next x,y based on the current position and the suggested move within the grid world.\n"
            f"The current position is: {current_position}\n"
            f"The visited positions are: {list(self.visited_positions)}\n"
            f"The last direction moved was: {self.last_suggestion}\n"
            f"The suggested move is: {move_direction}\n"
            f"Known obstacle positions: {list(self.obstacle_positions)}\n"
            f"DIRECTION MAPPING - YOU MUST FOLLOW EXACTLY:\n"
            f"- 'north' = move UP = [x-1, y]\n"
            f"- 'south' = move DOWN = [x+1, y]\n"
            f"- 'east' = move RIGHT = [x, y+1]\n"
            f"- 'west' = move LEFT = [x, y-1]\n"
            f"- 'northeast' = move UP-RIGHT = [x-1, y+1]\n"
            f"- 'northwest' = move UP-LEFT = [x-1, y-1]\n"
            f"- 'southeast' = move DOWN-RIGHT = [x+1, y+1]\n"
            f"- 'southwest' = move DOWN-LEFT = [x+1, y-1]\n"
            f"RULES:\n"
            f"1. The next position should be within the grid world (0-9 for both x and y).\n"
            f"2. The next position shouldn't be a visited position unless necessary.\n"
            f"3. The next position MUST NOT be an obstacle position.\n"
            f"4. STRICTLY follow the suggested move direction.\n"
            f"5. IMPORTANT: Avoid returning to the previous position. Do not repeat the last direction moved unless necessary.\n"
            f"6. MOST IMPORTANT: Only move in the direction suggested by the seeker - this is based on clues about where the treasure is located.\n"
            f"\nFEW-SHOT EXAMPLES:\n"
            f"Current position: [0, 0], Move: east → Next position: [0, 1]\n"
            f"Current position: [1, 1], Move: south → Next position: [2, 1]\n" 
            f"Current position: [2, 2], Move: northeast → Next position: [1, 3]\n"
            f"Current position: [5, 5], Move: southwest → Next position: [6, 4]\n"
            f"Current position: [9, 9], Move: north → Next position: [8, 9]\n"
            f"Current position: [0, 9], Move: west → Next position: [0, 8]\n"
            f"Current position: [3, 3], Move: south → Next position: [4, 3]\n"
            f"Current position: [5, 5], Move: southwest → Next position: [6, 4]\n"
            f"\nReturn ONLY a JSON object with the following structure:\n"
            f"{{\n"
            f"  \"position\": [x, y]\n"
            f"}}\n"
            f"Where x and y are integers between 0 and 9.\n"
            f"Example: {{\"position\": [3, 4]}}\n"
            f"IMPORTANT: Return ONLY the JSON object with no additional text or explanation. No markdown, no plain text, no extra commentary.\n"
        )

        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                response_json = json.loads(json_str)
                new_position = response_json.get("position", [])
                log(f"[DEBUG] Navigator response: {new_position}")
            else:
                response_json = json.loads(response.strip())
                new_position = response_json.get("position", [])
                log(f"[DEBUG] Navigator response: {new_position}")
            
            if isinstance(new_position, list) and len(new_position) == 2:
                x = max(0, min(9, int(new_position[0])))
                y = max(0, min(9, int(new_position[1])))
                new_position = [x, y]
                
                if tuple(new_position) in self.obstacle_positions:
                    log(f"[WARNING] Navigator tried to move onto obstacle at {new_position}, staying at {current_position}")
                    new_position = current_position
            else:
                new_position = current_position
        except (json.JSONDecodeError, ValueError):
            new_position = current_position
           
        self.last_suggestion = move_direction
        self.suggestion_history.append(move_direction)
        return new_position
