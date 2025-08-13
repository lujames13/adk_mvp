# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Google ADK (Agent Development Kit) MVP project that demonstrates multi-agent AI system architecture. The project implements specialized agents for search and financial analysis, coordinated by an LLM coordinator agent, all built using Google's ADK framework and Gemini models.

## Architecture

### Agent Hierarchy
- **Root Agent**: `search_agent` - Default entry point for ADK runtime
- **LLM Coordinator**: `llm_coordinator` - Orchestrates multiple specialized agents
- **Specialized Agents**:
  - `search_agent` - Google Search integration with `google_search` tool
  - `financial_agent` - Financial analysis (no tools, LLM-only)

### Project Structure
```
adk_mvp/
├── agent.py              # Main coordinator and root agent definition
├── prompt.py             # LLM coordinator prompt
└── sub_agents/
    ├── search_agent/     # Google Search specialized agent
    │   ├── agent.py      # Agent definition with google_search tool
    │   └── prompt.py     # Search-specific instructions
    └── financial_agent/  # Financial analysis specialized agent
        ├── agent.py      # Agent definition (LLM-only)
        └── prompt.py     # Financial analysis instructions
```

## Common Development Commands

### Environment Management
```bash
# Install dependencies (Poetry project)
poetry install

# Run the ADK agent (uses root_agent)
poetry run adk run adk_mvp

# Run tests
poetry run pytest tests/ -v

# Run specific test
poetry run pytest tests/test_agent.py::test_agent_initialization -v
```

### Google Cloud Setup
Required for Gemini model access:
```bash
# Authenticate
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable customsearch.googleapis.com
gcloud services enable generativelanguage.googleapis.com

# Check authentication status
gcloud auth list
gcloud config list
```

### Environment Variables
Create `.env` file:
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Technical Details

### Model Configuration
- All agents use `gemini-2.0-flash` model
- Region: Configured via `GOOGLE_CLOUD_LOCATION` (prefer `us-central1` for model availability)
- Falls back to `gemini-1.5-pro` if newer models unavailable in region

### Agent Design Patterns
1. **Specialized Agents**: Each agent has focused responsibility (search vs financial)
2. **Tool Integration**: Only search_agent has tools; financial_agent is LLM-only
3. **Coordinator Pattern**: LLM coordinator determines which agents to use
4. **Prompt Separation**: Each agent has dedicated prompt files for maintainability

### Testing Strategy
- Unit tests verify agent initialization and tool availability
- Tests check model configuration and tool integration
- Functional testing requires actual API calls (marked accordingly)

### Dependencies
- `google-adk`: Core ADK framework (>=1.10.0)
- `google-cloud-aiplatform`: Vertex AI integration (>=1.108.0) 
- `google-genai`: Gemini model access (>=1.29.0)
- `pydantic`: Data validation (>=2.11.7)
- `python-dotenv`: Environment configuration (>=1.1.1)

## Development Considerations

### Root Agent Selection
The `root_agent = search_agent` assignment determines which agent ADK launches by default. To change the entry point, modify this assignment in `agent.py`.

### Adding New Agents
1. Create new subdirectory in `sub_agents/`
2. Implement `agent.py` with Agent configuration
3. Create `prompt.py` with agent instructions
4. Import and register in main `agent.py`
5. Add to LLM coordinator tools if needed

### Model Availability Issues
If encountering 404 errors for models:
1. Check model availability in your configured region
2. Consider switching to `gemini-1.5-pro` (more widely available)
3. Verify `GOOGLE_CLOUD_LOCATION` environment variable

### Debugging
- ADK logs available at `/tmp/agents_log/agent.latest.log`
- Use `poetry env info` to verify Python environment
- Check GCP authentication with `gcloud auth list`