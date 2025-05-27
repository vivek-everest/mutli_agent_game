import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log(message, ui_only=False):
    """Log a message to both file and UI if specified.
    
    Args:
        message (str): The message to log
        ui_only (bool): If True, only log to UI, not to file
    """
    if not ui_only:
        logger.info(message)
    
    if 'messages' in st.session_state:
        st.session_state.messages.append(message)
        if len(st.session_state.messages) > 10:  
            st.session_state.messages.pop(0)

def agent_log(agent_id, message):
    print(f"[{agent_id}] {message}")
