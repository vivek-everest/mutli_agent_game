from llm.openai_wrapper import call_gpt
from agents.base_navigator import BaseNavigatorAgent
import json
from utils.logger import log

class NavigatorAgentWithoutObstacles(BaseNavigatorAgent):
    def __init__(self, name="Navigator"):
        super().__init__(name)
    
    def getNextPosition(self, current_position, move_direction, environment_data=None):
        """Get the next position based on the move."""
        self.visited_positions.add(tuple(current_position))
        
        position_history = list(self.visited_positions)[-5:] if len(self.visited_positions) > 5 else list(self.visited_positions)
        
        prompt = (
            f"You are a navigator agent in a 10x10 grid world treasure hunt game.\n"
            f"Your job is to calculate the EXACT next position based on the current position and direction.\n\n"
            f"Current position: {current_position}\n"
            f"Suggested move direction: {move_direction}\n"
            f"Previously visited positions: {position_history}\n"
            f"Last suggested direction: {self.last_suggestion}\n\n"
            f"EXACT DIRECTION VECTORS - YOU MUST USE THESE:\n"
            f"- north = [-1,0] (move up)\n"
            f"- northeast = [-1,1] (move up and right)\n" 
            f"- east = [0,1] (move right)\n"
            f"- southeast = [1,1] (move down and right)\n"
            f"- south = [1,0] (move down)\n"
            f"- southwest = [1,-1] (move down and left)\n"
            f"- west = [0,-1] (move left)\n"
            f"- northwest = [-1,-1] (move up and left)\n\n"
            f"STRICT RULES:\n"
            f"1. Apply the EXACT direction vector to the current position (add the vector to the coordinates)\n"
            f"2. Stay within grid bounds (0-9 for both x and y)\n"
            f"3. NEVER return to any previously visited position\n"
            f"4. If the exact move would revisit a position, make the SMALLEST possible adjustment to the vector\n"
            f"5. ALWAYS prioritize movement in the primary direction (e.g., for 'south', prioritize moving down)\n"
            f"6. NEVER move in the opposite direction of what was suggested\n\n"
            f"EXAMPLES WITH CALCULATIONS:\n"
            f"Current: [5,5], Direction: east → Vector [0,1] → [5,5] + [0,1] = [5,6]\n"
            f"Current: [0,0], Direction: south → Vector [1,0] → [0,0] + [1,0] = [1,0]\n"
            f"Current: [3,3], Direction: southeast → Vector [1,1] → [3,3] + [1,1] = [4,4]\n"
            f"Current: [9,9], Direction: southwest → Cannot apply [1,-1] due to bounds → Use [0,-1] instead → [9,8]\n\n"
            f"If position [4,4] was visited and current is [3,3] with southeast direction:\n"
            f"1. Calculate: [3,3] + [1,1] = [4,4]\n"
            f"2. Since [4,4] was visited, adjust to [4,5] or [5,4] instead\n\n"
            f"Return ONLY a JSON object with this structure: {{\"position\": [x, y]}}\n"
            f"Ensure it's a valid, unvisited position following the direction vector rules above.\n"
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
                
                if tuple(new_position) in self.visited_positions:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            test_pos = [max(0, min(9, x + dx)), max(0, min(9, y + dy))]
                            if tuple(test_pos) not in self.visited_positions and test_pos != current_position:
                                new_position = test_pos
                                break
            else:
                new_position = current_position
        except (json.JSONDecodeError, ValueError):
            new_position = current_position
           
        self.last_suggestion = move_direction
        self.suggestion_history.append(move_direction)
        return new_position
