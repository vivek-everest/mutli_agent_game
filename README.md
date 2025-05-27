# Treasure Hunt Game Exercise

This is a treasure hunt game where a seeker agent works with a navigator agent to find a hidden treasure in a grid world. The game has two versions: with and without obstacles.

## Exercise Overview

This project is designed as an exercise for learning about agent-based systems. Your task is to implement the missing functionality in the seeker and navigator agents to make them successfully find the treasure.

## Game Versions

### With Obstacles
- Grid contains randomly placed obstacles
- Agent must navigate around obstacles
- Game ends if agent gets trapped

### Without Obstacles
- Clean grid with no obstacles
- Focus on efficient treasure hunting

## Project Structure

- `agents/`: Contains agent implementations
  - `base_agent.py`: Base class for seeker agents
  - `base_navigator.py`: Base class for navigator agents
  - `with_obstacles/`: Implementations for the game with obstacles
  - `without_obstacles/`: Implementations for the game without obstacles
- `games/`: Contains game environments and UI
- `llm/`: Contains LLM wrappers for agent decision making
- `utils/`: Utility functions

## Implementation Tasks

Your main tasks in this exercise are to implement:

1. The `decide_move` method in seeker agents to determine direction based on clues
2. The `getNextPosition` method in navigator agents to calculate position updates

All the required method signatures are already provided with TODO comments.

## Running the Game

1. Install the requirements: `pip install -r requirements.txt`
2. Set up your OpenAI API key in a `.env` file: `OPENAI_API_KEY=your_api_key_here`
3. Run the main script: `python main.py`
4. Choose a game version from the UI

## Data Flow

1. Environment provides view data to the seeker
2. Seeker decides on a move direction based on the view
3. Navigator calculates the next position based on the move direction
4. Environment updates and the cycle continues until the treasure is found

## Game Controls
- Time Limit: Adjust the time limit for the game
- New Game: Start a new game
- Stop: End the current game 