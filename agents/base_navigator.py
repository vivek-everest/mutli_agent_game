class BaseNavigatorAgent:
    def __init__(self, name="Navigator"):
        self.name = name
        self.visited_positions = set()
        self.last_suggestion = None
        self.suggestion_history = []
        self.obstacle_positions = set()
    
    def getNextPosition(self, current_position, move_direction, environment_data=None):
        """
        Calculate the next position based on the current position and move direction.
        
        Args:
            current_position (list): Current position [x, y]
            move_direction (str): Direction to move ('north', 'south', 'east', 'west', etc.)
            environment_data (dict, optional): Additional environment data including:
                - 'visible_obstacles': List of visible obstacle positions
                - 'grid_size': Size of the grid [width, height]
                - Any other environment-specific data
                
        Returns:
            list: Next position [x, y]
        """
        raise NotImplementedError("Subclasses must implement getNextPosition.")
    
    def get_state(self):
        """
        Get the current state of the navigator for UI display or other external use.
        
        Returns:
            dict: Navigator state data including:
                - 'name': Navigator name
                - 'visited_positions': Set of visited positions
                - 'last_suggestion': Last direction suggested
                - Any other navigator-specific state data
        """
        return {
            'name': self.name,
            'visited_positions': list(self.visited_positions),
            'last_suggestion': self.last_suggestion,
            'suggestion_history': self.suggestion_history,
            'obstacle_positions': list(self.obstacle_positions)
        }
    
    def update_environment_data(self, environment_data):
        """
        Update the navigator's knowledge of the environment.
        
        Args:
            environment_data (dict): Environment data including:
                - 'visible_obstacles': List of visible obstacle positions
                - Any other environment-specific data
        """
        if environment_data and 'visible_obstacles' in environment_data:
            self.obstacle_positions.update(map(tuple, environment_data['visible_obstacles']))
    