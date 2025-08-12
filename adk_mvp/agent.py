# adk_mvp/agent.py

from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.0-flash"

search_agent = Agent(
    model=MODEL,
    name="search_agent",
    instruction=prompt.SEARCH_AGENT_PROMPT,
    tools=[google_search],
)

# 這是 ADK 會尋找的主要 agent
root_agent = search_agent