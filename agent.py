import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load OpenRouter API key from Streamlit secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Define the LLM using OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"  # You can also use "openai/gpt-3.5-turbo"
)

# Define the tool logic
def basic_tool(location, soil, crop):
    return f"""
📍 Location: {location}
🧪 Soil Type: {soil}
🌱 Crop: {crop}

🗓️ Farming Plan:
- Prepare land with compost and tilling.
- Sow {crop} seeds 7–10 days from now.
- Schedule irrigation based on rainfall.
- Monitor for pests during week 3.
"""

# Define as a LangChain Tool
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")) if len(x.split("|")) == 3 else "Invalid input format. Use: location|soil|crop",
        description="Generates a sowing and irrigation calendar based on location, soil, and crop. Input format: location|soil|crop"
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# This function is called from main.py
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    prompt = f"Use the KrishiCalendarTool on this input: {query}"
    return agent.invoke({"input": prompt})
