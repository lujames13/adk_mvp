# adk_mvp/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from . import prompt
from .sub_agents import search_agent, financial_agent

MODEL = "gemini-2.0-flash"

llm_coordinator = LlmAgent(
    model=MODEL,
    name="llm_coordinator",
    instruction=prompt.LLM_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=financial_agent),
    ],
)

# 這是 ADK 會尋找的主要 agent
root_agent = llm_coordinator