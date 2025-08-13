# adk_mvp/sub_agents/financial_agent/agent.py
from google.adk import Agent
from . import prompt

MODEL = "gemini-2.0-flash"

financial_agent = Agent(
    model=MODEL,
    name="financial_agent",
    instruction=prompt.FINANCIAL_AGENT_PROMPT,
) 