import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load OpenRouter API key
api_key = st.secrets["OPENROUTER_API_KEY"]

# Setup LLM from OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"  # works fine with REACT agent
)

# Tool function
def basic_tool(location, soil, crop):
    return f"""
📍 **Location:** {location}  
🧪 **Soil Type:** {soil}  
🌾 **Crop:** {crop}  

🗓️ **AI-Generated Krishi Calendar**:

| Week | Activity                                |
|------|-----------------------------------------|
| 1    | Land preparation, ploughing             |
| 2    | Apply organic compost                   |
| 3    | Seed treatment and sowing of {crop}     |
| 4    | First irrigation (based on {soil} soil) |
| 5    | Weed management                         |
| 6-7  | Fertilizer application                  |
| 8-10 | Pest & disease monitoring               |
| 12+  | Harvesting (depending on crop maturity) |

💡 *Consult your KVK or agri-extension officer for local support.*
"""

# Define the tool
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")) if len(x.split("|")) == 3 else "❌ Invalid input format. Use: location|soil|crop",
        description="Use this tool to generate a farming calendar for a specific crop. Input format: location|soil|crop"
    )
]

# Agent using REACT-based decision-making (no function calling)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Function called from main.py
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(query)
