from agents.base_agent import BaseAgent
from llm.openai_wrapper import call_gpt
import json
from utils.logger import log

class ClueAnalyzerAgent:
    """Agent responsible for analyzing clues and extracting direction and distance information."""
    
    def analyze(self, clue):
        """Extract direction and distance information from the clue using LLM."""
        prompt = (
            f"You are a specialized agent that analyzes clues in a treasure hunt game.\n"
            f"Given the following clue, extract the directional information and distance indicators.\n\n"
            f"Clue: \"{clue}\"\n\n"
            f"Analyze this clue and extract:\n"
            f"1. The direction(s) where the treasure is located (north, south, east, west, northeast, northwest, southeast, southwest)\n"
            f"2. Any distance indicators (very close, nearby, getting warmer, far)\n"
            f"3. Any obstacles mentioned and their directions\n\n"
            f"Return ONLY a JSON object with this format:\n"
            f"{{\"directions\": [list of directions], \"distance\": \"distance indicator\", \"obstacles_mentioned\": [list of directions with obstacles]}}\n"
        )
        
        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                extracted_info = json.loads(json_str)
            else:
                extracted_info = json.loads(response.strip())
                
            log(f"[DEBUG] ClueAnalyzer extracted: {extracted_info}")
            return extracted_info
        except Exception as e:
            log(f"[ERROR] ClueAnalyzer error: {e}")
            return {
                "directions": [],
                "distance": None,
                "obstacles_mentioned": []
            }


class MapperAgent:
    """Agent responsible for maintaining and updating the map of the environment."""
    
    def __init__(self):
        self.obstacle_positions = set()
        self.visited_positions = set()
        self.move_history = []
        
    def update_map(self, current_pos, visible_obstacles=None):
        """Update the map with new information."""
        self.visited_positions.add(current_pos)
        self.move_history.append(current_pos)
        
        if visible_obstacles:
            self.obstacle_positions.update(map(tuple, visible_obstacles))
            
        prompt = (
            f"You are a mapping agent in a treasure hunt game. Analyze the current map state:\n"
            f"Current position: {current_pos}\n"
            f"Recently visited positions: {self.move_history[-5:] if len(self.move_history) > 5 else self.move_history}\n"
            f"Known obstacles: {list(self.obstacle_positions)}\n\n"
            f"Based on this information, provide insights about:\n"
            f"1. Any patterns in movement (are we going in circles?)\n"
            f"2. Areas that might be worth exploring\n"
            f"3. Potential obstacle clusters to avoid\n\n"
            f"Return ONLY a JSON object with this format:\n"
            f"{{\"movement_pattern\": \"description\", \"exploration_suggestions\": [\"areas\"], \"obstacle_clusters\": [\"regions\"]}}\n"
        )
        
        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                map_analysis = json.loads(json_str)
            else:
                map_analysis = json.loads(response.strip())
                
            log(f"[DEBUG] Mapper analysis: {map_analysis}")
            return map_analysis
        except Exception as e:
            log(f"[ERROR] Mapper error: {e}")
            return {
                "movement_pattern": "unknown",
                "exploration_suggestions": [],
                "obstacle_clusters": []
            }
    
    def get_next_position(self, current_pos, direction):
        """Calculate the next position based on direction."""
        x, y = current_pos
        if direction == "north":
            return (x-1, y)
        elif direction == "south":
            return (x+1, y)
        elif direction == "west":
            return (x, y-1)
        elif direction == "east":
            return (x, y+1)
        elif direction == "northeast":
            return (x-1, y+1)
        elif direction == "northwest":
            return (x-1, y-1)
        elif direction == "southeast":
            return (x+1, y+1)
        elif direction == "southwest":
            return (x+1, y-1)
        return current_pos


class PathfinderAgent:
    """Agent responsible for finding paths around obstacles."""
    
    def __init__(self, mapper):
        self.mapper = mapper
        
    def get_available_moves(self, current_pos):
        """Get list of available moves using LLM reasoning."""
        prompt = (
            f"You are a pathfinder agent in a treasure hunt game. You need to determine available moves.\n"
            f"Current position: {current_pos}\n"
            f"Known obstacles: {list(self.mapper.obstacle_positions)}\n"
            f"The grid is 10x10 with indices from 0 to 9.\n\n"
            f"Analyze which of the following directions are available without hitting obstacles or going out of bounds:\n"
            f"- north (x-1, y)\n"
            f"- south (x+1, y)\n"
            f"- east (x, y+1)\n"
            f"- west (x, y-1)\n"
            f"- northeast (x-1, y+1)\n"
            f"- northwest (x-1, y-1)\n"
            f"- southeast (x+1, y+1)\n"
            f"- southwest (x+1, y-1)\n\n"
            f"Return ONLY a JSON object with this format:\n"
            f"{{\"available_moves\": [\"list of available directions\"]}}\n"
        )
        
        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                result = json.loads(json_str)
                available_moves = result.get("available_moves", [])
            else:
                result = json.loads(response.strip())
                available_moves = result.get("available_moves", [])
                
            log(f"[DEBUG] Available moves: {available_moves}")
            return available_moves
        except Exception as e:
            log(f"[ERROR] Pathfinder available moves error: {e}")
            available = []
            directions = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
            for direction in directions:
                next_pos = self.mapper.get_next_position(current_pos, direction)
                if next_pos not in self.mapper.obstacle_positions and 0 <= next_pos[0] < 10 and 0 <= next_pos[1] < 10:
                    available.append(direction)
            return available
    
    def find_path_around_obstacles(self, current_pos, clue_info):
        """Find a path around obstacles to reach the target direction."""
        prompt = (
            f"You are an AI pathfinder helping a treasure seeker navigate around obstacles.\n"
            f"Current position: {current_pos}\n"
            f"Directional clue: {clue_info['directions']}\n"
            f"Distance indicator: {clue_info.get('distance')}\n"
            f"Known obstacles: {list(self.mapper.obstacle_positions)}\n"
            f"Visited positions: {list(self.mapper.visited_positions)}\n"
            f"Move history: {self.mapper.move_history[-5:] if len(self.mapper.move_history) > 5 else self.mapper.move_history}\n\n"
            f"The treasure seeker wants to move in the direction(s) {clue_info['directions']} but may be blocked by obstacles.\n"
            f"Your task is to suggest the SINGLE next move that will help navigate around obstacles while generally moving toward the treasure.\n"
            f"Rules:\n"
            f"1. NEVER suggest a move into a known obstacle.\n"
            f"2. Prefer moves that align with the clue direction when possible.\n"
            f"3. If the direct path is blocked, suggest a detour that will eventually lead in the target direction.\n"
            f"4. Avoid positions that have been visited many times before unless necessary.\n"
            f"5. If completely stuck, suggest any valid move to a non-obstacle position.\n"
            f"6. The grid is 10x10 with indices from 0 to 9.\n"
            f"7. When navigating around obstacles, consider whether it's better to go clockwise or counter-clockwise.\n\n"
            f"Return ONLY a JSON object with the format: {{\"direction\": \"<direction>\", \"reasoning\": \"brief explanation\"}}\n"
            f"Where direction is one of: north, south, east, west, northeast, northwest, southeast, southwest.\n"
        )
        
        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                result = json.loads(json_str)
                direction = result.get("direction", "").lower()
                reasoning = result.get("reasoning", "")
                log(f"[DEBUG] Pathfinder suggested: {direction}, reasoning: {reasoning}")
                return direction
            else:
                result = json.loads(response.strip())
                direction = result.get("direction", "").lower()
                reasoning = result.get("reasoning", "")
                log(f"[DEBUG] Pathfinder suggested: {direction}, reasoning: {reasoning}")
                return direction
        except Exception as e:
            log(f"[ERROR] Failed to parse pathfinder response: {e}")
            available = self.get_available_moves(current_pos)
            return available[0] if available else "north"


class NavigationAgent:
    """Agent responsible for making the final navigation decision."""
    
    def __init__(self, mapper, pathfinder):
        self.mapper = mapper
        self.pathfinder = pathfinder
        self.last_direction = None
        
    def decide_move(self, clue_info, current_pos, map_analysis, available_moves):
        """Make the final navigation decision using LLM."""
        prompt = (
            f"You are the main navigation decision-maker in a treasure hunt game with obstacles.\n\n"
            f"CURRENT STATE:\n"
            f"- Current position: {current_pos}\n"
            f"- Directional clue: {clue_info.get('directions', [])}\n"
            f"- Distance indicator: {clue_info.get('distance')}\n"
            f"- Obstacles mentioned in clue: {clue_info.get('obstacles_mentioned', [])}\n"
            f"- Map analysis: {map_analysis}\n"
            f"- Available moves: {available_moves}\n"
            f"- Known obstacles: {list(self.mapper.obstacle_positions)}\n"
            f"- Recent movement history: {self.mapper.move_history[-5:] if len(self.mapper.move_history) > 5 else self.mapper.move_history}\n"
            f"- Last direction moved: {self.last_direction}\n\n"
            
            f"DECISION GUIDELINES:\n"
            f"1. PRIORITIZE moving in a direction mentioned in the clue.\n"
            f"2. STRICTLY FOLLOW THE DIRECTION FROM THE CLUE, unless there's an obstacle or it would lead to revisiting the same positions repeatedly.\n"
            f"3. NEVER MOVE TOWARD A KNOWN OBSTACLE.\n"
            f"4. If the clue direction is blocked by an obstacle, try another available direction that still generally moves toward the treasure.\n"
            f"5. If completely stuck or in a loop, choose ANY unblocked direction to get unstuck.\n"
            f"6. For diagonal clues (like northeast), consider either moving diagonally or in one of the component directions (north or east).\n\n"
            
            f"Using all this information, determine the SINGLE BEST move to make next.\n\n"
            f"Return ONLY a JSON object with this format:\n"
            f"{{\"direction\": \"chosen direction\", \"explanation\": \"brief explanation of your choice\"}}\n"
        )
        
        response = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                result = json.loads(json_str)
                direction = result.get("direction", "").lower()
                explanation = result.get("explanation", "")
            else:
                result = json.loads(response.strip())
                direction = result.get("direction", "").lower()
                explanation = result.get("explanation", "")
                
            log(f"[DEBUG] Navigation decision: {direction}, reason: {explanation}")
            self.last_direction = direction
            return direction
        except Exception as e:
            log(f"[ERROR] Navigation decision error: {e}")
            direction = self.pathfinder.find_path_around_obstacles(current_pos, clue_info)
            self.last_direction = direction
            return direction


class SeekerAgentWithObstacles(BaseAgent):
    """A multi-agent seeker system for navigating grid worlds with obstacles."""
    
    def __init__(self, name, start_position):
        super().__init__(name, start_position)
        self.clue_analyzer = ClueAnalyzerAgent()
        self.mapper = MapperAgent()
        self.pathfinder = PathfinderAgent(self.mapper)
        self.navigation_agent = NavigationAgent(self.mapper, self.pathfinder)
        self.trapped_count = 0
        
    def decide_move(self, view_data):
        """
        Process the environment view and decide on the next move.
        
        Args:
            view_data (dict): Data about the current environment view
        
        Returns:
            str: Direction to move
        """
        self.visited_positions.add(tuple(self.position))
        
        clue = view_data.get("clue", "")
        visible_obstacles = view_data.get("visible_obstacles", [])
        
        clue_info = self.clue_analyzer.analyze(clue)
        
        self.mapper.visited_positions = self.visited_positions  
        self.mapper.move_history = self.position_history + [self.position] 
        map_analysis = self.mapper.update_map(tuple(self.position), visible_obstacles)
        
        available_moves = self.pathfinder.get_available_moves(tuple(self.position))
        
        if not available_moves:
            self.trapped_count += 1
            if self.trapped_count >= 3:  
                return "trapped"
            
            for direction in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
                next_pos = self.mapper.get_next_position(tuple(self.position), direction)
                if next_pos not in self.mapper.obstacle_positions and 0 <= next_pos[0] < 10 and 0 <= next_pos[1] < 10:
                    return direction
            
            return "trapped"
        
        self.trapped_count = 0
        
        direction = self.navigation_agent.decide_move(clue_info, tuple(self.position), map_analysis, available_moves)
        
        self.last_direction = direction
        self.move_history.append(direction)
        
        return direction 