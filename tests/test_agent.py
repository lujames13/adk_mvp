# tests/test_agent.py

import pytest
from adk_mvp.agent import root_agent

def test_agent_initialization():
    """測試 agent 是否正確初始化"""
    assert root_agent.name == "search_agent"
    assert root_agent.model == "gemini-2.5-pro"
    assert len(root_agent.tools) > 0

def test_agent_has_search_tool():
    """測試 agent 是否包含搜尋工具"""
    tool_names = [tool.__class__.__name__ for tool in root_agent.tools]
    # 檢查是否有搜尋相關的工具
    assert any("search" in name.lower() for name in tool_names)

# 註：實際的搜尋測試需要真實的 API 調用，我們先確保基本結構正確