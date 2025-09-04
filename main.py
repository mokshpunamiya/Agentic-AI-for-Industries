import os
import streamlit as st
from dotenv import load_dotenv

from data_manager import DataManager
from tools import AnalysisToolkit
from agent import AgentSystem
from ui import PSUInterface

# Load environment variables
load_dotenv()


def main():
    # Set page configuration
    st.set_page_config(page_title="Agentic AI Interface", layout="wide")

    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Enter your OpenRouter API key:", type="password")
        if not api_key:
            st.error("API key is required to continue.")
            st.stop()

    # Initialize data
    data_manager = DataManager()
    df = data_manager.load_data()

    # Initialize tools and agent
    tools = AnalysisToolkit(df)
    agent_system = AgentSystem(api_key, tools)

    # Initialize UI
    app = PSUInterface(df, agent_system)
    app.run()


if __name__ == "__main__":
    main()
