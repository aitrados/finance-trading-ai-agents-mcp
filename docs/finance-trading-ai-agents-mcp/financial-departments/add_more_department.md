---
weight: 1000
date: "2025-09-04T10:00:00+01:00"
draft: false
author: "VON"
title: "Add More Department"
icon: "article"
toc: true
description: "Add More Department MCP SERVER"
publishdate: "2025-09-13T10:00:00+01:00"
tags: ["Add More Department MCP SERVER", "MCP SERVER", "Add MCP SERVER"]
---


```python
from fastmcp import Context, FastMCP
from typing import List
from pydantic import Field

from finance_trading_ai_agents_mcp.addition_custom_mcp.addition_custom_mcp_interface import AdditionCustomMcpInterface

from finance_trading_ai_agents_mcp.mcp_services.economic_calendar_service import mcp as economic_calendar_mcp
from finance_trading_ai_agents_mcp.mcp_services.news_service import mcp as news_mcp
from finance_trading_ai_agents_mcp.mcp_services.price_action_service import mcp as price_action_mcp
from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_service import mcp as traditional_indicator_mcp

class AdditionCustomMcpExample(AdditionCustomMcpInterface):
    def add_mcp_server_name(self)->FastMCP:
        ## http://127.0.0.1:11999/mcp_servers.json and see the custom_mcp_server1 server
        mcp = FastMCP("custom_mcp_server1")
        @mcp.tool(title="custom_mcp_server_name")
        async def get_custom_abc(context: Context, full_symbol: str = "STOCK:US:AAPL", interval: str = "DAY"):
            return f"Custom indicator data for {full_symbol} on {interval}"
        return mcp
```

## Full EXAMPLES

https://github.com/aitrados/finance-trading-ai-agents-mcp/tree/main/examples/addition_custom_mcp_examples
