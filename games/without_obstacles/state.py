class GameStateWithoutObstacles:
    def __init__(self):
        self.found = False
        self.treasure_position = None
        self.moves = []

    def set_treasure_found(self, position):
        self.found = True
        self.treasure_position = position

    def log_move(self, agent_id, position, direction):
        self.moves.append({
            "agent": agent_id,
            "position": position,
            "direction": direction
        }) 