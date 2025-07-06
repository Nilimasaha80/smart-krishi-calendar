import streamlit as st
import json
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load API key
api_key = st.secrets["OPENROUTER_API_KEY"]

# Load expert calendar data for Etawah
with open("crop_practices_etawah.json") as f:
    crop_data = json.load(f)

# Get calendar entry based on crop, soil, and location
def get_calendar_entry(crop, soil, location):
    try:
        entry = crop_data[crop][soil][location]
        lines = [
            f"📍 **Location:** {location}",
            f"🧪 **Soil Type:** {soil}",
            f"🌾 **Crop:** {crop}",
            f"\n🗓️ **Expert Farming Calendar**\n"
        ]
        for i, week in enumerate(entry["calendar"], 1):
            lines.append(f"**Week {i}:** {week}")
        lines.append(f"\n🌤️ **Weather Suitability:** {entry['weather_conditions']}")
        lines.append("\n✅ *This is an expert-generated plan for Etawah. Always verify with local KVK or extension officer.*")
        return "\n".join(lines)
    except KeyError:
        return f"❌ No data available for {crop} in {location} with {soil} soil. Try a different input."

# Tool wrapper

def wrapped_tool(input_str):
    parts = input_str.split("|")
    if len(parts) != 3:
        return "❌ Format error: Use location|soil|crop"
    return get_calendar_entry(parts[2].strip(), parts[1].strip(), parts[0].strip())

# Define tool for the agent
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=wrapped_tool,
        description="Returns an expert-level farming calendar for the given crop, soil, and district. Format: location|soil|crop"
    )
]

# Define LLM for agent
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"
)

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Main callable function for streamlit app
def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use KrishiCalendarTool with this input: {query}")
