import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load your OpenRouter API key from Streamlit secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Initialize the LLM from OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"  # You can switch to gpt-3.5 etc.
)

# Function that returns the Krishi Calendar
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

💡 *This is a general calendar. For exact timings, consult local agri-extension officers or KVK experts.*
"""

# Tool definition
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")) if len(x.split("|")) == 3 else "❌ Invalid input format. Use: location|soil|crop",
        description="Generates a sowing and irrigation calendar. Format: location|soil|crop"
    )
]

# Initialize the agent with tool + LLM
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# This is the function called from main.py
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    prompt = f"Use the KrishiCalendarTool on this input: {query}"
    return agent.invoke({"input": prompt})
