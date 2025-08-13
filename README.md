# ADK MVP - Multi-Agent System

A Google ADK (Agent Development Kit) MVP project demonstrating multi-agent AI system architecture with specialized agents for search and financial analysis.

## Overview

This project implements a coordinated multi-agent system using Google's ADK framework and Gemini models. It features an LLM coordinator that orchestrates specialized agents, each optimized for specific tasks.

## Architecture

### Agent Hierarchy
- **Root Agent**: `llm_coordinator` - Main entry point orchestrating specialized agents
- **Specialized Agents**:
  - `search_agent` - Google Search integration with `google_search` tool
  - `financial_agent` - Financial analysis (LLM-only, no tools)

### Project Structure
```
adk_mvp/
├── adk_mvp/
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # LLM coordinator and root agent
│   ├── prompt.py             # Coordinator prompt
│   └── sub_agents/           # Specialized agents
│       ├── search_agent/     # Google Search agent
│       │   ├── agent.py      # Agent with google_search tool
│       │   └── prompt.py     # Search-specific instructions
│       └── financial_agent/  # Financial analysis agent
│           ├── agent.py      # LLM-only agent
│           └── prompt.py     # Financial analysis instructions
├── tests/
│   └── test_agent.py         # Agent tests
├── .env                      # Environment configuration
├── pyproject.toml            # Poetry dependencies
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud account with billing enabled
- Poetry for dependency management

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd adk_mvp
poetry install
```

2. **Google Cloud setup**:
```bash
# Authenticate
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable customsearch.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

3. **Environment configuration**:
Create `.env` file:
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Running the System

```bash
# Start the multi-agent system
poetry run adk run adk_mvp

# Run tests
poetry run pytest tests/ -v
```

## How It Works

### Multi-Agent Coordination

The system uses a coordinator pattern where:

1. **User Query** → `llm_coordinator` (root agent)
2. **Coordinator** analyzes the query and determines which specialist agent to use
3. **Specialist Agent** processes the request using its tools/expertise
4. **Response** flows back through the coordinator to the user

### Agent Capabilities

#### LLM Coordinator
- Routes queries to appropriate specialist agents
- Combines responses from multiple agents when needed
- Handles general queries that don't require specialized tools

#### Search Agent  
- Performs web searches using Google Search API
- Provides current information and fact-checking
- Cites sources with URLs

#### Financial Agent
- Analyzes financial data and trends
- Provides investment insights and market analysis
- Pure LLM-based reasoning (no external tools)

## Technical Details

### Model Configuration
- All agents use `gemini-2.0-flash` model by default
- Falls back to `gemini-1.5-pro` if newer models unavailable
- Configured via environment variables for different regions

### Dependencies
```toml
[tool.poetry.dependencies]
python = "^3.9"
google-adk = ">=1.10.0"
google-cloud-aiplatform = ">=1.108.0" 
google-genai = ">=1.29.0"
pydantic = ">=2.11.7"
python-dotenv = ">=1.1.1"
```

### Testing
```bash
# Run all tests
poetry run pytest tests/ -v

# Test specific functionality  
poetry run pytest tests/test_agent.py::test_agent_initialization -v
```

## Usage Examples

### Starting the System
```bash
poetry run adk run adk_mvp
# Output: Running agent llm_coordinator, type exit to exit.
```

### Example Queries

**Search-related queries** (routed to search_agent):
- "What are the latest AI developments in 2024?"
- "Current weather in San Francisco"
- "Recent Python best practices"

**Financial queries** (routed to financial_agent):
- "Analyze the current market trends"
- "What factors affect stock volatility?"
- "Explain cryptocurrency market dynamics"

**General queries** (handled by coordinator):
- "Hello, how can you help me?"
- "What agents are available?"

## Development

### Adding New Agents

1. Create agent directory in `sub_agents/`:
```bash
mkdir adk_mvp/sub_agents/new_agent
```

2. Implement agent files:
```python
# sub_agents/new_agent/agent.py
from google.adk.agents import LlmAgent

new_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="new_agent", 
    instruction="Agent instructions here",
    tools=[]  # Add tools if needed
)

# sub_agents/new_agent/prompt.py
NEW_AGENT_PROMPT = """
Your agent instructions here...
"""
```

3. Register in main coordinator:
```python
# adk_mvp/agent.py
from .sub_agents import new_agent

llm_coordinator = LlmAgent(
    model=MODEL,
    name="llm_coordinator",
    instruction=prompt.LLM_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=financial_agent),
        AgentTool(agent=new_agent),  # Add here
    ],
)
```

### Best Practices

- **Start Simple**: Begin with LLM-only agents before adding tools
- **Single Responsibility**: Each agent should have a focused purpose  
- **Test First**: Write tests before implementing functionality
- **Error Handling**: Implement robust error handling for production use

## Troubleshooting

### Common Issues

**Model Not Available Error**:
```
google.genai.errors.ClientError: 404 NOT_FOUND
Publisher Model `gemini-2.0-flash` not found in [region]
```
**Solution**: Change `GOOGLE_CLOUD_LOCATION` to `us-central1` or use `gemini-1.5-pro`

**Authentication Issues**:
```bash
# Re-authenticate
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**Dependency Conflicts**:
```bash
# Clear cache and reinstall
poetry cache clear PyPI --all
poetry install --no-cache
```

### Useful Commands

```bash
# Development
poetry install                           # Install dependencies
poetry run pytest tests/ -v             # Run tests  
poetry run adk run adk_mvp              # Start agents

# Google Cloud
gcloud auth list                         # Check auth status
gcloud services list --enabled          # View enabled APIs
gcloud config list                       # View configuration

# Debugging  
poetry env info                          # Environment info
tail -F /tmp/agents_log/agent.latest.log # View logs
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
