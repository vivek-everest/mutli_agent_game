class BaseAgent:
    def __init__(self, name, start_position):
        self.name = name
        self.position = start_position
        self.visited_positions = set([tuple(start_position)])
        self.last_direction = None
        self.move_history = []
        self.position_history = []

    def decide_move(self, view_data):
        """
        Process the environment view and decide on the next move.
        
        Args:
            view_data (dict): Data about the current environment view including:
                - 'clue': String clue about treasure direction/distance
                - 'treasure_found': Boolean indicating if treasure is found
                - 'visible_obstacles': List of obstacle positions visible from current position
                - Any other environment-specific data
                
        Returns:
            str: Direction to move ('north', 'south', 'east', 'west', etc.) or 'trapped' if no moves available
        """
        raise NotImplementedError("Subclasses must implement decide_move.")
    
    def get_state(self):
        """
        Get the current state of the agent for UI display or other external use.
        
        Returns:
            dict: Agent state data including:
                - 'name': Agent name
                - 'position': Current position
                - 'visited_positions': Set of visited positions
                - 'move_history': List of previous moves
                - Any other agent-specific state data
        """
        return {
            'name': self.name,
            'position': self.position,
            'visited_positions': list(self.visited_positions),
            'last_direction': self.last_direction,
            'move_history': self.move_history,
            'position_history': self.position_history
        }
    
    def update_position(self, new_position):
        """
        Update the agent's position based on navigator's calculation.
        
        Args:
            new_position (list): New position [x, y]
        """
        self.position = new_position
        self.visited_positions.add(tuple(new_position))
        self.position_history.append(new_position)
