class GameStateWithObstacles:
    def __init__(self):
        self.found = False
        self.treasure_position = None
        self.moves = []
        self.obstacle_positions = set()
        self.is_trapped = False

    def set_treasure_found(self, position):
        self.found = True
        self.treasure_position = position

    def set_trapped(self):
        self.is_trapped = True

    def log_move(self, agent_id, position, direction):
        self.moves.append({
            "agent": agent_id,
            "position": position,
            "direction": direction
        })

    def update_obstacles(self, obstacles):
        self.obstacle_positions = set(obstacles) 