import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# 📦 Crop calendar data for Etawah district (soil-wise + crop-wise)
crop_data = {
    "wheat": {
        "Loamy": {
            "Etawah": {
                "calendar": [
                    "Ploughing and harrowing",
                    "Apply compost and basal fertilizers",
                    "Sowing (Nov 10–25)",
                    "Irrigation at CRI stage",
                    "Weed removal (30 DAS)",
                    "Top dressing with nitrogen",
                    "Rust and aphid control",
                    "Harvest in April (around 25% moisture)"
                ],
                "weather_conditions": "Cool dry winters (15–25°C)"
            }
        },
        "Clayey": {
            "Etawah": {
                "calendar": [
                    "Deep ploughing, good drainage needed",
                    "Balanced fertilizer with potash",
                    "Seed treatment for fungus",
                    "Proper spacing (22 cm rows)",
                    "Top dressing in two splits",
                    "Harvest in mid-April"
                ],
                "weather_conditions": "Clay retains moisture but risks waterlogging"
            }
        }
    },
    "rice": {
        "Clayey": {
            "Etawah": {
                "calendar": [
                    "Field puddling, bunding",
                    "FYM + green manure",
                    "Transplanting (June 15–July 5)",
                    "Standing water irrigation",
                    "Weed removal, zinc application",
                    "Pest management (BPH, blast)",
                    "Top dressing of urea",
                    "Harvest by October end"
                ],
                "weather_conditions": "Heavy rainfall required; 1000mm+"
            }
        },
        "Loamy": {
            "Etawah": {
                "calendar": [
                    "Fine tilth preparation",
                    "Use of short-duration paddy",
                    "SRI method for higher yield",
                    "Irrigation every 7 days",
                    "Harvest early October"
                ],
                "weather_conditions": "Monsoon-dependent, watch for lodging"
            }
        }
    },
    "mustard": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Light ploughing",
                    "Sowing (Oct 15–Nov 5)",
                    "No standing water",
                    "Foliar spray of boron",
                    "Early harvest (Feb end)"
                ],
                "weather_conditions": "Grows well in low moisture"
            }
        },
        "Loamy": {
            "Etawah": {
                "calendar": [
                    "Balanced fertilization",
                    "Closer spacing for weed control",
                    "Watch for aphids",
                    "Irrigate at flowering"
                ],
                "weather_conditions": "Moderate moisture required"
            }
        }
    },
    "maize": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Summer ploughing",
                    "Sowing with spacing 60x20 cm",
                    "2 irrigations (knee height & tasseling)",
                    "Detasseling for hybrids",
                    "Harvest before drying"
                ],
                "weather_conditions": "Needs warm, dry weather"
            }
        }
    }
    # Add more crops here as needed
}

# 🔑 Load OpenRouter API key
api_key = st.secrets["OPENROUTER_API_KEY"]

# 🤖 LLM setup
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"
)

# 🌾 Expert crop planner tool
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

# 🪰 Tool wrapper
def wrapped_tool(input_str):
    parts = input_str.split("|")
    if len(parts) != 3:
        return "❌ Format error: Use location|soil|crop"
    return expert_calendar_tool(parts[0], parts[1], parts[2])

# 🛠️ Tool definition
tools = [
    Tool(
        name="KrishiCalendarTool",
        func=wrapped_tool,
        description="Generates an expert farming calendar for Etawah. Format: location|soil|crop"
    )
]

# 🧠 Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🚀 Main function

def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(query)
