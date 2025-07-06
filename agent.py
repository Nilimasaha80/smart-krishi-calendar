import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load OpenRouter API key securely from Streamlit Secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Set up the LLM (ChatOpenAI-style wrapper, pointing to OpenRouter)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"  # or "openai/gpt-3.5-turbo"
)

# Define a simple tool
def basic_tool(location, soil, crop):
    return f"For {location} with {soil} soil, growing {crop}, prepare land, apply compost, and sow in 10 days."

tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")),
        description="Suggests a crop plan for a given location, soil, and crop"
    )
]

# Initialize agent with the tool
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Function that main.py can call
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use KrishiCalendarTool to plan sowing for {crop} in {location} with {soil} soil.")
