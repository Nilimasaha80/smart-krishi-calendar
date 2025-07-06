import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load API key
api_key = st.secrets["OPENROUTER_API_KEY"]

# Set up OpenRouter-compatible LLM
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"
)

# Calendar generation logic
def basic_tool(location, soil, crop):
    return f"""
📍 **Location:** {location}  
🧪 **Soil Type:** {soil}  
🌾 **Crop:** {crop}  

🗓️ **Smart Krishi Calendar**

| Week | Activity                                |
|------|-----------------------------------------|
| 1    | Land preparation, ploughing             |
| 2    | Apply organic compost                   |
| 3    | Seed treatment and sowing of {crop}     |
| 4    | First irrigation (based on {soil} soil) |
| 5    | Weed management                         |
| 6-7  | Fertilizer application                  |
| 8-10 | Pest & disease monitoring               |
| 12+  | Harvesting based on local conditions    |

✅ *This plan is AI-assisted. Please consult local KVK or extension workers.*
"""

# Tool to parse "Etawah|Sandy|Rice" format
def wrapped_tool(input_str):
    parts = input_str.split("|")
    if len(parts) != 3:
        return "❌ Format error: Use location|soil|crop"
    return basic_tool(parts[0], parts[1], parts[2])

tools = [
    Tool(
        name="KrishiCalendarTool",
        func=wrapped_tool,
        description="Generates a farming calendar for a given location, soil type, and crop. Format: location|soil|crop"
    )
]

# Use REACT agent (OpenRouter safe)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function to use in main.py
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use KrishiCalendarTool with this input: {query}")
