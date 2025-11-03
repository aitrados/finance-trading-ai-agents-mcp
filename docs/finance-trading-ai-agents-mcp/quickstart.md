---
weight: 100
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "MCP Quickstart"
icon: "rocket_launch"
toc: true
description: "A free, specialized MCP server for financial analysis and quantitative trading. Provides one-click setup for local financial MCP services with department-based architecture simulating financial company operations. Supports traditional indicators, price action analysis, economic calendar, fundamental analysis, and news integration for seamless LLM interaction and algorithmic trading."
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["finance mcp","financial mcp", "finance agent","streaming ohlc", "trading mcp", "ai trading","ai mcp"]
---

A free, professional, open-source financial analysis and quantitative trading MCP server. It lets you deploy a local financial MCP service with one command, using a departmental architecture that simulates a real financial firm's operations. It supports traditional indicators, price action analysis, economic calendar, fundamentals, and news integration—providing seamless interaction with LLMs and algorithmic trading.

## ✨ Features

- 🚀 One-click deployment: Quickly spin up a local financial MCP service
- 🏢 Departmental architecture: Simulates real-world financial company departments
- 📊 Comprehensive analysis: Traditional technical indicators + price action analysis
- 📅 Real-time data: Economic calendar, fundamentals, and news integration
- 🤖 AI integration: Interfaces optimized for LLMs
- ⚡ High performance: Real-time streaming OHLC data processing
- 🔧 Extensible: Support for custom MCP services

## GitHub
- Repository: https://github.com/aitrados/finance-trading-ai-agents-mcp
- Embed system prompts into your LLM (e.g., LangChain): https://github.com/aitrados/finance-trading-ai-agents-mcp/tree/main/basic_system_prompt_words
- Simple examples: https://github.com/aitrados/finance-trading-ai-agents-mcp/tree/main/examples

## 1. Installation
- Recommended (PyPI):
```bash
pip install finance-trading-ai-agents-mcp
```

## 2. Fastest path to run (Python)
Save the following as main.py and run it:

```python
from finance_trading_ai_agents_mcp import mcp_run
from examples.env_example import get_example_env

if __name__ == "__main__":
    get_example_env()  # write example environment variables
    mcp_run()  # start the MCP service
```
After it starts, open your browser at: http://127.0.0.1:11999/

Tip: You need a free AITRADOS_SECRET_KEY to access financial data → https://www.aitrados.com/

<img src="/mcp-homepage.png" alt="Homepage image" style="max-width: 100%; height: auto;" />

## 3. Command-line (CLI) one-liners
- Show help:
```bash
finance-trading-ai-agents-mcp --help
```
- Quick start (minimal config):
```bash
finance-trading-ai-agents-mcp --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}
```
- Specify port:
```bash
python -m finance_trading_ai_agents_mcp -p 9000 --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}
```
- Use a custom MCP capability file:
```bash
python -m finance_trading_ai_agents_mcp -c examples/addition_custom_mcp_examples/addition_custom_mcp_example.py --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}
```

## 4. Required environment configuration (minimal)
Create a .env file in the project root (or pass values via --env-config):
```env
# Debug
DEBUG=true
# Get for free at https://www.aitrados.com/
AITRADOS_SECRET_KEY=YOUR_SECRET_KEY

# Max number of OHLC rows for LLM output only (does not affect strategy calculations)
OHLC_LIMIT_FOR_LLM=30
# Rename the column name from interval to timeframe (example)
RENAME_COLUMN_NAME_MAPPING_FOR_LLM=interval:timeframe,
# Minimal columns to provide to the LLM
OHLC_COLUMN_NAMES_FOR_LLM=timeframe,close_datetime,open,high,low,close,volume
```
Advanced options (optional):
- LIVE_STREAMING_OHLC_LIMIT defaults to 150; if you need long-period indicators like MA200, increase it appropriately.

## 5. A few advanced steps (optional)
- Custom MCP services and functions:

```python
from finance_trading_ai_agents_mcp import mcp_run
from examples.env_example import get_example_env

if __name__ == "__main__":
    get_example_env()
    from examples.addition_custom_mcp_examples.addition_custom_mcp_example import AdditionCustomMcpExample

    AdditionCustomMcpExample()
    mcp_run()
```
- Reuse real-time WebSocket data + MCP simultaneously: see examples/run_mcp_examples/run_mcp_with_callback_real_time_websocks_data_example.py

## 6. Documentation and examples
- Full docs: https://docs.aitrados.com
- GitHub: https://github.com/aitrados/finance-trading-ai-agents-mcp

— You're all set. Start the service and let AI and real-time financial data work seamlessly in your workflow.