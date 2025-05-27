import streamlit as st
import os
import sys
from utils.logger import log

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

def main():
    if 'game_type' not in st.session_state:
        st.session_state.game_type = None

    if st.session_state.game_type == "with_obstacles":
        from games.with_obstacles.ui import main as with_obstacles_main
        with_obstacles_main()
        return
    elif st.session_state.game_type == "without_obstacles":
        from games.without_obstacles.ui import main as without_obstacles_main
        without_obstacles_main()
        return

    st.title("Treasure Hunt Game")
    st.write("Choose a version of the game to play:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play With Obstacles"):
            for key in list(st.session_state.keys()):
                if key != 'game_type':
                    del st.session_state[key]
            st.session_state.game_type = "with_obstacles"
            log("Starting game with obstacles")
            st.experimental_rerun()
    with col2:
        if st.button("Play Without Obstacles"):
            for key in list(st.session_state.keys()):
                if key != 'game_type':
                    del st.session_state[key]
            st.session_state.game_type = "without_obstacles"
            log("Starting game without obstacles")
            st.experimental_rerun()
    st.write("---")
    st.write("### Game Versions")
    st.write("#### With Obstacles")
    st.write("""
    - Grid contains randomly placed obstacles
    - Agent must navigate around obstacles to find the treasure
    - More challenging gameplay with strategic pathfinding
    - Game ends if agent gets trapped
    """)
    st.write("#### Without Obstacles")
    st.write("""
    - Clean grid with no obstacles
    - Focus on efficient treasure hunting
    - Simpler gameplay with pure navigation
    - Perfect for learning the basics
    """)

if __name__ == "__main__":
    main()
