---
weight: 400
date: "2025-09-05T11:00:00+01:00"
draft: false
author: "VON"
title: "Traditional Indicator  department"
icon: "analytics"
toc: true
description: "Provides calculation and querying of common technical indicators (MA, RSI, MACD, BOLL) with OHLC data (MCP tool call)."
publishdate: "2025-09-14T11:00:00+01:00"
tags: ["Traditional Indicator", "Technical Analysis", "MCP", "LLM", "MA", "RSI", "MACD", "BOLL"]
---

The Traditional Technical Indicators module provides candlestick (OHLC) data for financial products and, based on this, calculates common technical analysis indicators such as Moving Averages (MA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Bollinger Bands (BOLL). It is suitable for quantitative trading, chart analysis, and market research.

Tip: Before use, please complete the Quickstart or ensure the service is running, and configure `AITRADOS_SECRET_KEY` in your `.env` file.

## Available MCP Tools
- get_traditional_indicators
  - Purpose: To get integrated data containing OHLC and specified technical indicators.
  - Core parameters:
    - `full_symbol`: Financial product symbol (e.g., "STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD").
    - `interval`: Timeframe (e.g., "DAY", "HOUR", "M30", "M15", "M5", "M1").
    - `indicators`: List of indicators to calculate (optional values: "MA", "RSI", "MACD", "BOLL"), maximum of 4.
    - `ma_periods`: List of periods for the moving average (e.g., [5, 10, 20]), maximum of 10.
    - `limit`: Number of data rows to return, default is 150.
    - `format`: Output format ("csv" or "json").
    - `is_eth`: Whether to include US pre-market and after-hours data (True/False).

## Quick Examples
- Querying MA and RSI indicators for a stock (LLM prompt example):
  `Please call get_traditional_indicators, full_symbol="STOCK:US:AAPL", interval="DAY", indicators=["MA", "RSI"], ma_periods=[5, 20], limit=30, and return the data.`

- Querying using the Python/MCP client:
  `client.call_tool("get_traditional_indicators", {"full_symbol": "STOCK:US:AAPL", "interval": "DAY", "indicators": ["MA", "RSI", "MACD"], "ma_periods": [5, 10, 20], "limit": 50})`

## Return Data and Format
- The returned data includes the original OHLC data as well as the newly calculated indicator columns.
- Supports `csv` and `json` formats. If feeding to an LLM, `csv` is recommended to reduce context usage.
- A clear error message will be returned if there is no data or a calculation error.

## Best Practices
- **Comprehensive Analysis**: Request multiple indicators at the same time (e.g., "MA" and "MACD") to perform trend and momentum analysis.
- **Multi-Period Strategy**: Set different lengths for moving averages (e.g., `[5, 60]`) via the `ma_periods` parameter to identify short-term and long-term trends.
- **Data Volume**: Ensure the `limit` parameter is large enough so that technical indicators (especially long-period ones) can be calculated effectively.
- **Precise Querying**: Specify `full_symbol` and `interval` to get the data that best fits your analysis needs.

## Add Custom Function Tools
- [Append custom function tools to the current MCP server](../custom_function_tool.md)

For more on running and environment configuration, please see the Quickstart.