import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
from games.with_obstacles.environment import GridWorldWithObstacles
from agents.with_obstacles.navigator import NavigatorAgentWithObstacles
from games.with_obstacles.state import GameStateWithObstacles
from utils.logger import log
from agents.with_obstacles.seeker import SeekerAgentWithObstacles

def initialize_game():
    st.session_state.env = GridWorldWithObstacles()
    st.session_state.seeker = SeekerAgentWithObstacles("A0", [0, 0])
    st.session_state.navigator = NavigatorAgentWithObstacles()
    st.session_state.state = GameStateWithObstacles()
    st.session_state.game_running = True
    st.session_state.start_time = time.time()
    st.session_state.game_result = None
    log(f"🎯 Treasure is hidden at position {st.session_state.env.treasure}")
    log(f"⏱️ Time limit: {st.session_state.time_limit} seconds")

def run_game_step():
    if not st.session_state.game_running:
        return

    elapsed_time = time.time() - st.session_state.start_time
    if elapsed_time >= st.session_state.time_limit:
        log(f"❌ Failed to find treasure within {st.session_state.time_limit} seconds")
        log(f"Final position: {st.session_state.seeker.position}")
        log(f"Treasure was at: {st.session_state.env.treasure}")
        log(f"Positions visited: {len(st.session_state.seeker.visited_positions)}")
        log(f"Time elapsed: {elapsed_time:.1f} seconds")
        st.session_state.game_running = False
        st.session_state.game_result = "timeout"
        return

    # Get current state from environment
    seeker = st.session_state.seeker
    navigator = st.session_state.navigator
    
    # Get environment view data
    view = st.session_state.env.get_view("A0", seeker.position)
    log(f"🔍 Seeker at {seeker.position}: {view['clue']}")
    
    # Check if treasure found
    if view["treasure_found"]:
        log(f"🎉 Treasure found at {seeker.position}")
        st.session_state.state.set_treasure_found(seeker.position)
        st.session_state.game_running = False
        st.session_state.game_result = "success"
        return
    
    # Seeker decides on move based on view data
    move = seeker.decide_move(view)
    log(f"🔍 Seeker suggested move: {move}")

    if move == "trapped":
        log(f"🚫 Agent is trapped at position {seeker.position}")
        log(f"Final position: {seeker.position}")
        log(f"Treasure was at: {st.session_state.env.treasure}")
        log(f"Positions visited: {len(seeker.visited_positions)}")
        log(f"Time elapsed: {elapsed_time:.1f} seconds")
        st.session_state.game_running = False
        st.session_state.game_result = "trapped"
        return
    
    # Navigator calculates next position based on seeker's move
    environment_data = {
        'visible_obstacles': view.get("visible_obstacles", []),
        'grid_size': [10, 10]
    }
    
    new_position = navigator.getNextPosition(seeker.position, move, environment_data)
    
    # Update seeker's position
    seeker.update_position(new_position)
    
    # Update game state
    st.session_state.state.log_move("A0", new_position, move)
    log(f"Seeker moved {move} to {new_position}")

    # Check if treasure found at new position
    found = st.session_state.env.check_treasure(new_position)
    
    if found:
        log(f"🎉 Treasure found at {seeker.position}")
        st.session_state.state.set_treasure_found(seeker.position)
        st.session_state.game_running = False
        st.session_state.game_result = "success"
        return

def draw_grid():
    grid = np.zeros((10, 10))
    
    for obs_pos in st.session_state.env.obstacles:
        grid[obs_pos[0], obs_pos[1]] = 2  
    
    treasure_pos = st.session_state.env.treasure
    grid[treasure_pos[0], treasure_pos[1]] = 3 
    
    seeker_pos = st.session_state.seeker.position
    grid[seeker_pos[0], seeker_pos[1]] = 1 
    
    for pos in st.session_state.seeker.visited_positions:
        if grid[pos[0], pos[1]] == 0:  
            grid[pos[0], pos[1]] = 0.5  
    
    return grid

def main():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'game_running' not in st.session_state:
        st.session_state.game_running = False
    if 'env' not in st.session_state:
        st.session_state.env = None
    if 'seeker' not in st.session_state:
        st.session_state.seeker = None
    if 'navigator' not in st.session_state:
        st.session_state.navigator = None
    if 'state' not in st.session_state:
        st.session_state.state = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_limit' not in st.session_state:
        st.session_state.time_limit = 60
    if 'game_result' not in st.session_state:
        st.session_state.game_result = None

    st.title("Treasure Hunt Game (With Obstacles)")
    
    with st.sidebar:
        st.header("Game Controls")
        if st.button("New Game"):
            initialize_game()
        if st.button("Back to Main Menu"):
            st.session_state.game_type = None
            st.experimental_rerun()
        
        st.header("Game Settings")
        time_limit = st.slider("Time Limit (seconds)", 30, 180, 60)
        if time_limit != st.session_state.time_limit:
            st.session_state.time_limit = time_limit
            if st.session_state.game_running:
                log(f"⏱️ Time limit updated: {time_limit} seconds")
        
        st.header("Colors")
        st.markdown("🔴 Seeker - Red")
        st.markdown("🧭 Navigator - Blue (suggestions)")
        st.markdown("💎 Treasure - Green")
        st.markdown("⚫ Obstacles - Black")
        st.markdown("⚪ Visited - Light Gray")
        
        if st.session_state.game_result:
            st.header("Game Statistics")
            elapsed_time = time.time() - st.session_state.start_time
            if st.session_state.game_result == "success":
                st.success(f"✅ Found treasure in {elapsed_time:.1f} seconds!")
            elif st.session_state.game_result == "trapped":
                st.error(f"🚫 Agent is trapped at position {st.session_state.seeker.position}")
            else:
                st.error(f"❌ Failed to find treasure in {elapsed_time:.1f} seconds")
            st.metric("Positions Visited", len(st.session_state.seeker.visited_positions))
            st.metric("Time Remaining", f"{max(0, st.session_state.time_limit - elapsed_time):.1f}s")
    
    col1, col2 = st.columns([4, 3])
    
    with col1:
        if st.session_state.env is not None:
            grid = draw_grid()
            fig = plt.figure(figsize=(8, 8))
            plt.imshow(grid, cmap='RdYlBu')
            plt.grid(True)
            plt.xticks(range(10))
            plt.yticks(range(10))
            plt.title("Treasure Hunt Grid")
            st.pyplot(fig)
            plt.close(fig)
    
    with col2:
        st.header("Game Messages")
        message_container = st.container(height=400)
        with message_container:
            for message in st.session_state.messages:
                st.markdown(f"<div style='word-wrap: break-word; white-space: pre-wrap;'>{message}</div>", unsafe_allow_html=True)
    
    if st.session_state.game_running:
        time.sleep(1) 
        run_game_step()
        st.rerun()

if __name__ == "__main__":
    main() 