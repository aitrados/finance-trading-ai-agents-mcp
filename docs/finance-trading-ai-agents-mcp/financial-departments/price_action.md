---
weight: 300
date: "2025-09-06T14:00:00+01:00"
draft: false
author: "VON"
title: "Price Action department"
icon: "candlestick_chart"
toc: true
description: "Provides basic OHLC candlestick data queries, supporting real-time and historical data retrieval for single or multiple symbols and timeframes (MCP tool call)."
publishdate: "2025-09-15T14:00:00+01:00"
tags: ["Price Action", "OHLC", "K-Line", "MCP", "LLM", "Streaming"]
---

The Price Action module is the foundation of all technical analysis, focusing on providing the core OHLC (Open, High, Low, Close) candlestick data. It supports fetching real-time and historical data for single or multiple financial products and can request multiple timeframes at once, making it a cornerstone for building trading strategies and performing market analysis.

Tip: Before use, please complete the Quickstart or ensure the service is running, and configure `AITRADOS_SECRET_KEY` in your `.env` file.

## Available MCP Tools
This module provides a series of tools to fetch candlestick data, ranging from simple historical data queries to complex multi-symbol, multi-timeframe real-time data streams.

- **get_latest_ohlc**
  - Purpose: Fetches the latest **historical** candlestick data for a specified financial product. This is a non-streaming, one-time request.
  - Core parameters:
    - `full_symbol`: The financial product symbol.
    - `interval`: The timeframe.
    - `limit`: The number of data rows to return (1-1000).
    - `format`: The output format (`csv` or `json`).
    - `is_eth`: Whether to include US pre-market and after-hours data.

- **get_live_streaming_ohlc**
  - Purpose: Gets **real-time streaming** candlestick data for a single symbol on a single timeframe.
  - Core parameters: Same as above, the `limit` parameter controls the number of bars returned at a time.

- **get_multi_timeframe_live_streaming_ohlc**
  - Purpose: Gets **real-time streaming** candlestick data for a single symbol across multiple timeframes.
  - Core parameters:
    - `full_symbol`: The financial product symbol.
    - `intervals`: A list of timeframes (e.g., `["M15", "M60", "DAY"]`).

- **get_multi_symbol_multi_timeframe_live_streaming_ohlc**
  - Purpose: Fetches **real-time streaming** candlestick data for multiple symbols and multiple timeframes at once, making it the most efficient monitoring tool.
  - Core parameters:
    - `item_data`: A dictionary to define the symbols and timeframes to subscribe to.

## Quick Examples
- Fetch latest historical candlesticks (LLM prompt example):
  `Please call get_latest_ohlc with full_symbol="STOCK:US:AAPL", interval="DAY", and limit=100.`

- Get real-time data for a single symbol across multiple timeframes (Python/MCP client):
  `client.call_tool("get_multi_timeframe_live_streaming_ohlc", {"full_symbol": "CRYPTO:GLOBAL:BTCUSD", "intervals": ["5M", "30M", "60M"]})`

- Get real-time data for multiple symbols and timeframes (Python/MCP client):
  ```python
  item_data = {
      "STOCK:US:AAPL": ["DAY", "60M"],
      "STOCK:US:TSLA": ["DAY", "60M"],
      "CRYPTO:GLOBAL:ETHUSD": ["15M", "60M"],
  }
  client.call_tool("get_multi_symbol_multi_timeframe_live_streaming_ohlc", {"item_data": item_data})
  ```

## Return Data and Format
- Data returned from all **streaming** functions will be separated by Markdown headings (e.g., `##### OHLC STOCK:US:AAPL -> DAY`) to clearly distinguish data for different symbols and timeframes.
- `get_latest_ohlc` directly returns a data string in the specified format (`csv` or `json`).
- A friendly prompt will be returned when no data is available.

## Best Practices
- **Historical Backtesting**: Use `get_latest_ohlc` with a large `limit` value to get ample historical data for strategy backtesting and model training.
- **Real-time Monitoring Dashboard**: Using `get_multi_symbol_multi_timeframe_live_streaming_ohlc` is the best choice for building real-time monitoring applications, as it can subscribe to all relevant market data with a single call.
- **Understanding the `item_data` Structure**: This is key to using the most advanced function, `get_multi_symbol_multi_timeframe_live_streaming_ohlc`. `item_data` is a dictionary where each key is a `full_symbol` string, and the corresponding value is a list of `interval` strings to subscribe to for that symbol.

## Add Custom Function Tools
- [Append custom function tools to the current MCP server](../custom_function_tool.md)

For more on running and environment configuration, please see the Quickstart.