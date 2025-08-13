# adk_mvp/sub_agents/search_agent/agent.py
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