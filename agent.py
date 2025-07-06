import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

api_key = st.secrets["OPENROUTER_API_KEY"]

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="mistralai/mistral-7b-instruct"
)

def basic_tool(location, soil, crop):
    return f"📍 Location: {location}\n🧪 Soil: {soil}\n🌱 Crop: {crop}\n\n🗓️ Plan:\n- Prepare land\n- Apply compost\n- Sowing in 10 days.\n- Irrigation after 5 days."

tools = [
    Tool(
        name="KrishiCalendarTool",
        func=lambda x: basic_tool(*x.split("|")) if len(x.split("|")) == 3 else "Invalid input format.",
        description="Takes input as 'location|soil|crop' and returns a basic farming calendar"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

def get_calendar_plan(location, soil, crop):
    query = f"{location}|{soil}|{crop}"
    return agent.run(f"Use the KrishiCalendarTool on this input: {query}")

fix: replaced agent.run with agent.invoke to support LangChain v0.1+
