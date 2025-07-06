import os
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool

# Load API key from env variable (add in Streamlit Cloud later)
llm = OpenAI(
    model_name="openai/gpt-3.5-turbo",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def basic_tool(location, soil, crop):
    return f"For {location} with {soil} soil, growing {crop}, prepare land, apply compost, and expect sowing in 10 days."

tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")),
        description="Suggests a crop plan for a given location, soil, and crop"
    )
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use KrishiCalendarTool to plan sowing for {crop} in {location} with {soil} soil.")
