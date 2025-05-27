import random
from utils.logger import log

class GridWorldWithObstacles:
    def __init__(self, size=(10, 10), obstacle_density=0.2):
        self.size = size
        self.treasure = [random.randint(0, size[0]-1), random.randint(0, size[1]-1)]
        self.obstacles = set()
        self._generate_obstacles(obstacle_density)
        log(f"🎯 Treasure is hidden at position {self.treasure}")
        log(f"🚧 Generated {len(self.obstacles)} obstacles")

    def _generate_obstacles(self, density):
        """Generate random obstacles, ensuring they don't block the treasure or starting position."""
        num_obstacles = int(self.size[0] * self.size[1] * density)
        while len(self.obstacles) < num_obstacles:
            pos = (random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1))
            if pos != tuple(self.treasure) and pos != (0, 0):
                self.obstacles.add(pos)

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

        # Get obstacles only in adjacent cells
        visible_obstacles = self._get_visible_obstacles(agent_position)
        
        # Only add obstacle information to the clue when there are actually adjacent obstacles
        if visible_obstacles:
            obstacle_directions = self._describe_obstacle_locations(agent_position, visible_obstacles)
            clue += f" There are obstacles {obstacle_directions}."

        return {
            "agent": agent_id,
            "position": agent_position,
            "treasure_found": treasure_found,
            "clue": clue,
            "distance": distance,
            "visible_obstacles": visible_obstacles
        }

    def _get_visible_obstacles(self, position):
        """Get obstacles visible from the current position (adjacent cells)."""
        x, y = position
        visible = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
                if (new_x, new_y) in self.obstacles:
                    visible.append((new_x, new_y))
        return visible

    def _describe_obstacle_locations(self, position, obstacles):
        """Describe the locations of visible obstacles relative to the current position."""
        x, y = position
        directions = []
        for obs_x, obs_y in obstacles:
            if obs_x < x and obs_y == y:
                directions.append("north")
            elif obs_x > x and obs_y == y:
                directions.append("south")
            elif obs_x == x and obs_y < y:
                directions.append("west")
            elif obs_x == x and obs_y > y:
                directions.append("east")
            elif obs_x < x and obs_y > y:
                directions.append("northeast")
            elif obs_x < x and obs_y < y:
                directions.append("northwest")
            elif obs_x > x and obs_y > y:
                directions.append("southeast")
            elif obs_x > x and obs_y < y:
                directions.append("southwest")
        return ", ".join(directions) if directions else "none"

    def is_valid_move(self, position, direction):
        x, y = position
        new_x, new_y = x, y
        
        if direction == "up": new_x = max(0, x - 1)
        elif direction == "down": new_x = min(self.size[0]-1, x + 1)
        elif direction == "left": new_y = max(0, y - 1)
        elif direction == "right": new_y = min(self.size[1]-1, y + 1)
            
        if (new_x, new_y) in self.obstacles:
            return position  
            
        return [new_x, new_y]

    def check_treasure(self, position):
        return self.treasure == position 