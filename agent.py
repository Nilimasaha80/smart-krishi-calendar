import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load OpenRouter API key securely from Streamlit Cloud secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Set up the LLM via OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"  # works well with REACT-style agent
)

# Tool function to return farming calendar
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

💡 *Consult your local KVK or agri-extension officer for hyperlocal guidance.*
"""

# Tool configuration
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")) if len(x.split("|")) == 3 else "❌ Format must be: location|soil|crop",
        description="Use this tool to generate a farming calendar. Format: location|soil|crop"
    )
]

# Set up the agent using REACT-style reasoning (safe for OpenRouter models)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Function used in main.py to trigger the tool
def get_calendar_plan(location, soil, crop):
    query = f"Use KrishiCalendarTool on this input: {location}|{soil}|{crop}"
    return agent.run(query)
