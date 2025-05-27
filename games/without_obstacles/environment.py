import random
from utils.logger import log

class GridWorldWithoutObstacles:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.treasure = [random.randint(0, size[0]-1), random.randint(0, size[1]-1)]
        log(f"🎯 Treasure is hidden at position {self.treasure}")

    def get_view(self, agent_id, agent_position):
        """Return limited view of the world with clues."""
        treasure_found = self.treasure == agent_position
        
        distance = abs(agent_position[0] - self.treasure[0]) + abs(agent_position[1] - self.treasure[1])
        
        if distance == 0:
            clue = "You found the treasure!"
        elif distance == 1:
            clue = "You're very close to the treasure!"
        elif distance <= 2:
            clue = "The treasure is nearby!"
        elif distance <= 3:
            clue = "You're getting warmer..."
        else:
            clue = "You're far from the treasure."

        if not treasure_found:
            dx = self.treasure[0] - agent_position[0]
            dy = self.treasure[1] - agent_position[1]
            direction = None
            if dx > 0 and dy > 0:
                direction = "southeast"
            elif dx > 0 and dy < 0:
                direction = "southwest"
            elif dx < 0 and dy > 0:
                direction = "northeast"
            elif dx < 0 and dy < 0:
                direction = "northwest"
            elif dx > 0:
                direction = "south"
            elif dx < 0:
                direction = "north"
            elif dy > 0:
                direction = "east"
            elif dy < 0:
                direction = "west"
            if direction:
                clue += f" The treasure is to the {direction}."

        return {
            "agent": agent_id,
            "position": agent_position,
            "treasure_found": treasure_found,
            "clue": clue,
            "distance": distance,
            "visible_obstacles": [] 
        }

    def is_valid_move(self, position, direction):
        """
        direction: one of 'up', 'down', 'left', 'right',
        'northeast', 'southeast', 'southwest', 'northwest'
        """
        x, y = position
        new_x, new_y = x, y
        
        if direction == "up": new_x = max(0, x - 1)
        elif direction == "down": new_x = min(self.size[0]-1, x + 1)
        elif direction == "left": new_y = max(0, y - 1)
        elif direction == "right": new_y = min(self.size[1]-1, y + 1)
        elif direction == "northeast":
            new_x = max(0, x - 1)
            new_y = min(self.size[1]-1, y + 1)
        elif direction == "southeast":
            new_x = min(self.size[0]-1, x + 1)
            new_y = min(self.size[1]-1, y + 1)
        elif direction == "southwest":
            new_x = min(self.size[0]-1, x + 1)
            new_y = max(0, y - 1)
        elif direction == "northwest":
            new_x = max(0, x - 1)
            new_y = max(0, y - 1)
        
        return [new_x, new_y]

    def check_treasure(self, position):
        return self.treasure == position 