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
        current_pos = tuple(self.position)
        self.visited_positions.add(current_pos)
        
        prompt = (
            f"You are a treasure seeker agent in a grid world of 10x10 without obstacles your name is {self.name} and you are in a treasure hunt game.\n"
            f"The treasure will be hidden in one of the 10x10 cells. You will be given a clue that will help you find the treasure.\n"
            f"The clue will be a direction or a combination of directions that will help you find the treasure. e.g. 'southeast', 'southwest', 'northeast', 'northwest', 'south', 'north', 'east', 'west'.\n"
            f"The Clue will also give you the distance as clue such as You're very close to the treasure!, The treasure is nearby!, You're getting warmer..., You're far from the treasure.\n"
            f"Your task is to find the next step to move towrds the treasure.\n"
            f"Each time you will get the current position, the clue and the visited positions. You have to find the next position to move towards the treasure.\n"
            f"Your current position: {self.position}\n"
            f"Current clue: {view_data['clue']}\n"
            f"All visited positions: {list(self.visited_positions)}\n\n"
            f"Last direction moved: {self.last_direction}\n"
            "RULES:\n"
            "1. ONLY move in a direction mentioned in the clue (e.g., if the clue says 'east' or 'northeast', only move east, right, or northeast).\n"
            "2. If the clue is a diagonal (e.g., 'northeast'), you may move diagonally (e.g., 'northeast') or either of the two cardinal directions (e.g., 'north' or 'east'), whichever is not visited.\n"
            "3. NEVER move in a direction not mentioned in the clue.\n"
            "Think step by step:\n"
            "1. What direction(s) does the clue indicate?\n"
            "2. Is that direction not visited?\n"
            "3. If not, what's the next best clue-aligned direction?\n\n"
            "Return ONLY a JSON object with the following structure:\n"
            "{\n"
            "  \"direction\": \"<direction>\"\n"
            "}\n"
            "Where <direction> is one of: 'southeast', 'southwest', 'northeast', 'northwest', 'south', 'north', 'east', 'west'.\n"
            "Example: {\"direction\": \"north\"}\n"
            "IMPORTANT: Return ONLY the JSON object with no additional text or explanation No markdown, no plain text, no extra commentary.\n"
        )
        move = call_gpt(prompt)
        
        try:
            import re
            json_match = re.search(r'({.*?})', move, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                response_json = json.loads(json_str)
                move = response_json.get("direction", "").lower()
                log(f"[DEBUG] Seeker move: {move}")
            else:
                response_json = json.loads(move.strip())
                move = response_json.get("direction", "").lower()
                log(f"[DEBUG] Seeker move: {move}")
        except json.JSONDecodeError:
            move = move.strip().lower()
            directions = ['southeast', 'southwest', 'northeast', 'northwest', 'south', 'north', 'east', 'west']
            for direction in directions:
                if direction in move:
                    move = direction
                    log(f"[DEBUG] Extracted direction from text: {move}")
                    break
       
        self.last_direction = move
        self.move_history.append(move)
        return move