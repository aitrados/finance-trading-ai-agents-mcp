---
weight: 200
date: "2025-09-04T10:00:00+01:00"
draft: false
author: "VON"
title: "News department"
icon: "article"
toc: true
description: "Provides the latest financial news, with support for retrieval by symbol (MCP tool call)."
publishdate: "2025-09-13T10:00:00+01:00"
tags: ["News", "News MCP", "Fundamental", "MCP", "LLM"]
---

The news module provides the latest news for specified financial products, suitable for scenarios like market sentiment analysis and event-driven trading.

Tip: Before use, please complete the Quickstart or ensure the service is running, and configure `AITRADOS_SECRET_KEY` in your `.env` file.

## API Data Source
https://docs.aitrados.com/en/docs/api/news/latest_news_list/


## Available MCP Tools
- get_latest_news_list
  - Purpose: To query the latest news list for a specified financial symbol.
  - Core parameters:
    - `full_symbol`: Financial product symbol (e.g., "STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD").
    - `limit`: The number of news articles to return, defaults to 5.

## Quick Example
- Querying the latest news for a stock (LLM prompt example):
  `Please call get_latest_news_list with full_symbol="STOCK:US:AAPL" and limit=3 to return the 3 latest news articles.`

- Querying using the Python/MCP client:
  `client.call_tool("get_latest_news_list", {"full_symbol": "STOCK:US:AAPL", "limit": 3})`

## Return Data and Format
- The returned data format is optimized for LLM consumption.
- A friendly message will be returned when no data is available (e.g., `No recent news found.`).

## Best Practices
- **Event-Driven Analysis**: Get the latest news for a specific stock or cryptocurrency to understand events that might affect its price.
- **Market Sentiment Monitoring**: Combine with other tools to analyze news content and assess the current market sentiment for an asset.
- **Control Information Volume**: Use the `limit` parameter to adjust the number of news articles retrieved, avoiding information overload and focusing on the most important ones.

## Add Custom Function Tools
- [Append custom function tools to the current MCP server](../custom_function_tool.md)

For more on running and environment configuration, please see the Quickstart.