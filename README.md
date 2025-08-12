# ADK MVP - Development Journey

> 從零開始構建 Google ADK Agent 的完整開發過程

## 項目概述

這是一個記錄從零開始使用 Google ADK (Agent Development Kit) 開發 AI Search Assistant 的完整過程。本項目展示了如何在現代 Python 開發環境中，從環境設置到成功運行的每一個步驟。

## 開發歷程

### 階段 1: 環境設置與項目初始化

#### 1.1 Poetry 項目初始化
```bash
# 創建項目目錄
mkdir adk_mvp && cd adk_mvp

# Poetry 交互式初始化
poetry init
```

**關鍵學習**:
- Poetry 2.0+ 移除了 `poetry shell` 命令
- 推薦使用 `poetry run` 來執行命令，避免環境污染
- 項目名稱可以使用連字符 (`adk-mvp`)，但 Python 包名必須使用下劃線 (`adk_mvp`)

#### 1.2 依賴管理策略
```toml
[tool.poetry.dependencies]
python = "^3.9"
google-adk = "^1.0.0"
google-cloud-aiplatform = {extras = ["agent-engines"], version = "^1.93.0"}
google-genai = "^1.9.0"
pydantic = "^2.10.6"
python-dotenv = "^1.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
pytest-asyncio = "^1.1.0"
```

**依賴安裝過程**:
```bash
poetry install
# 遇到錯誤: No file/folder found for package adk-mvp
# 解決: 創建正確的 Python 包結構
```

#### 1.3 項目結構設計
```
adk_mvp/
├── adk_mvp/              # Python 包 (使用下劃線)
│   ├── __init__.py
│   ├── agent.py
│   └── prompt.py
├── tests/
│   └── test_agent.py
├── .env                  # 環境變數
├── pyproject.toml        # Poetry 配置
└── README.md
```

**重要發現**: Poetry 要求項目具有有效的 Python 包結構才能完成安裝。

### 階段 2: Google Cloud 環境配置

#### 2.1 GCP 憑證設置
```bash
# 安裝 Google Cloud CLI
gcloud --version

# 認證流程
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

#### 2.2 API 啟用
```bash
# 啟用必要的 Google Cloud APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable customsearch.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

#### 2.3 環境變數配置
```bash
# .env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

**學習重點**: 地區選擇很重要，某些 AI 模型在特定地區不可用。

### 階段 3: 最簡 Agent 實現

#### 3.1 Prompt 設計 (`adk_mvp/prompt.py`)
```python
SEARCH_AGENT_PROMPT = """
You are a helpful search assistant powered by Google Search.

When a user asks a question:
1. Use the Google Search tool to find relevant and current information
2. Analyze the search results carefully
3. Provide a clear, informative answer based on the findings
4. Always cite your sources with URLs when possible
5. If you can't find relevant information, clearly state that

Be concise but comprehensive. Focus on accuracy and helpfulness.
"""
```

**設計原則**: 
- 明確定義 Agent 的行為
- 具體說明工具使用方式
- 強調準確性和來源引用

#### 3.2 Agent 實現 (`adk_mvp/agent.py`)
```python
from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.0-flash"  # 選擇穩定可用的模型

search_agent = Agent(
    model=MODEL,
    name="search_agent",
    instruction=prompt.SEARCH_AGENT_PROMPT,
    tools=[google_search],
)

root_agent = search_agent
```

**架構決策**:
- 單一工具整合 (Google Search)
- 簡潔的 Agent 結構

#### 3.3 包初始化 (`adk_mvp/__init__.py`)
```python
"""ADK MVP with Google Search functionality"""

from .agent import root_agent

__version__ = "0.1.0"
```

### 階段 4: 測試驅動驗證

#### 4.1 基礎測試實現
```python
# tests/test_agent.py
import pytest
from adk_mvp.agent import root_agent

def test_agent_initialization():
    """測試 agent 是否正確初始化"""
    assert root_agent.name == "search_agent"
    assert root_agent.model == "gemini-2.0-flash"
    assert len(root_agent.tools) > 0

def test_agent_has_search_tool():
    """測試 agent 是否包含搜尋工具"""
    tool_names = [tool.__class__.__name__ for tool in root_agent.tools]
    assert any("search" in name.lower() for name in tool_names)
```

#### 4.2 測試執行
```bash
poetry run pytest tests/ -v
# 結果: 2 passed, 1 warning in 5.46s
```

**測試策略**: 先確保基本結構正確，再進行功能測試。

### 階段 5: 問題排解與最佳化

#### 5.1 模型可用性問題
**遇到的錯誤**:
```
google.genai.errors.ClientError: 404 NOT_FOUND
Publisher Model `gemini-2.0-flash` not found in asia-east1
```

**解決方案**:
1. 調整地區設置: `us-central1`
2. 驗證模型可用性

#### 5.2 Poetry 工作流程適應
**Poetry 2.0+ 變化**:
- `poetry shell` → `poetry run` 或 `poetry env activate`
- 更強調依賴隔離
- 更適合 CI/CD 環境

**推薦工作流程**:
```bash
# 開發測試
poetry run python -m adk_mvp.agent
poetry run adk run adk_mvp
poetry run pytest tests/

# 依賴管理
poetry add new-package
poetry remove old-package
poetry show --tree
```

### 階段 6: 成功運行

#### 6.1 Agent 啟動
```bash
poetry run adk run adk_mvp
# 輸出: Running agent search_agent, type exit to exit.
```

#### 6.2 功能驗證
測試查詢範例:
- "What is the current weather in Taiwan?"
- "Tell me about recent AI developments"
- "Search for Python best practices 2024"

## 開發心得與最佳實踐

### 1. 環境管理
- **Poetry 2.0+**: 使用 `poetry run` 取代 `poetry shell`
- **依賴隔離**: 每個命令都明確在正確環境中執行
- **版本控制**: 精確指定依賴版本範圍

### 2. Google Cloud 整合
- **地區選擇**: 優先考慮模型可用性而非地理位置
- **API 啟用**: 提前啟用所有必要的 API
- **憑證管理**: 使用 `application-default` 認證

### 3. Agent 設計
- **簡潔原則**: 從最簡功能開始
- **工具整合**: 一次整合一個工具
- **測試先行**: 先確保基本結構，再添加功能

### 4. 問題排解策略
- **逐步驗證**: 每個階段都要驗證功能
- **日誌分析**: 善用 ADK 提供的日誌系統
- **模型降級**: 優先選擇穩定可用的模型

## 技術債務與改進方向

### 短期改進
- [ ] 添加更完整的錯誤處理
- [ ] 實現配置檔案管理
- [ ] 添加日誌級別控制

### 中期擴展
- [ ] 多工具整合 (計算機、天氣等)
- [ ] 會話記憶功能
- [ ] Web UI 介面

### 長期架構
- [ ] 多代理協作系統
- [ ] 插件化工具架構
- [ ] 生產環境部署流程

## 實用命令參考

```bash
# 開發環境
poetry install                           # 安裝依賴
poetry run pytest tests/ -v             # 運行測試
poetry run adk run adk_mvp              # 啟動 Agent

# Google Cloud
gcloud auth list                         # 檢查認證狀態
gcloud services list --enabled          # 查看已啟用的 API
gcloud config list                       # 查看配置

# 除錯
poetry env info                          # 查看環境資訊
tail -F /tmp/agents_log/agent.latest.log # 查看日誌
```

## 結語

這個 MVP 開發過程展示了現代 Python AI 應用開發的完整流程，從環境管理到雲端整合，從測試驗證到問題排解。每個步驟都記錄了實際遇到的問題和解決方案，為後續開發提供了寶貴的參考。

**核心收穫**: 
- 工具選擇的重要性 (Poetry 2.0+, ADK)
- 雲端服務整合的複雜性
- 測試驅動開發的價值
- 逐步迭代的開發方法論
