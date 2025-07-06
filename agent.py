import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Crop calendar data for Etawah district, soil-wise and crop-wise
crop_data = {
    "wheat": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Shallow ploughing and leveling",
                    "Apply FYM and phosphorus",
                    "Sowing in lines (Nov 1–15)",
                    "First irrigation at CRI stage (~21 DAS)",
                    "Weed management (30 DAS)",
                    "Top dressing with urea",
                    "Rust and aphid monitoring",
                    "Harvest in April (25% moisture)"
                ],
                "weather_conditions": "Cool dry winters, 15–25°C optimal"
            }
        }
        # Add Loamy and Clayey similarly...
    },
    "rice": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Land puddling & transplanting",
                    "High compost dose & FYM",
                    "Paddy transplanting (June–July)",
                    "Regular irrigation every 7 days",
                    "Weeding & zinc application",
                    "Pest (BPH) & blast watch",
                    "Top dressing with urea",
                    "Harvest in October"
                ],
                "weather_conditions": "Monsoon cropping, needs 1000mm+ rain"
            }
        }
        # Add Loamy and Clayey similarly...
    }
    # Add other crops here...
}

# Load OpenRouter API key
api_key = st.secrets["OPENROUTER_API_KEY"]

# Configure OpenRouter-compatible LLM
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"
)

# Expert calendar logic using data

def expert_calendar_tool(location, soil, crop):
    crop = crop.lower()
    soil = soil.capitalize()
    location = location.capitalize()

    if crop not in crop_data:
        return f"❌ Crop '{crop}' not supported yet."
    if soil not in crop_data[crop]:
        return f"❌ Soil type '{soil}' not available for crop '{crop}'."
    if location not in crop_data[crop][soil]:
        return f"❌ Location '{location}' not supported for crop '{crop}' with soil '{soil}'."

    calendar_info = crop_data[crop][soil][location]
    calendar = calendar_info["calendar"]
    weather = calendar_info["weather_conditions"]

    table = "\n".join([f"| Week {i+1} | {activity} |" for i, activity in enumerate(calendar)])
    return f"""
📍 **Location:** {location}  
🧪 **Soil Type:** {soil}  
🌾 **Crop:** {crop.capitalize()}  

🗓️ **Smart Krishi Calendar**

{table}

🌦️ *Weather Note:* {weather}  
✅ *Expert AI plan. Confirm with KVK/local extension staff.*
"""

# Tool wrapper

def wrapped_tool(input_str):
    parts = input_str.split("|")
    if len(parts) != 3:
        return "❌ Format error: Use location|soil|crop"
    return expert_calendar_tool(parts[0], parts[1], parts[2])

# Define tool

tools = [
    Tool(
        name="KrishiCalendarTool",
        func=wrapped_tool,
        description="Generates an expert farming calendar for a given location, soil type, and crop. Format: location|soil|crop"
    )
]

# Initialize agent

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function used in Streamlit main.py

def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use KrishiCalendarTool with this input: {query}")

