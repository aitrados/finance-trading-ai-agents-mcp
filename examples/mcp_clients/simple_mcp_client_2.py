import asyncio
import json

from aitrados_api.common_lib.contant import IntervalName
from fastmcp import Client

from finance_trading_ai_agents_mcp import analysis_department

from finance_trading_ai_agents_mcp.assistive_tools.assistive_tools_utils import get_client_mcp_config
from finance_trading_ai_agents_mcp.assistive_tools.mcp_tools_converter import LlmCallToolConverter

departments=[
 analysis_department.TRADITIONAL_INDICATOR
]
mcp_config=get_client_mcp_config(departments,mcp_base_url="http://127.0.0.1:11999")
print("Departments",list(mcp_config["mcpServers"].keys()))
print("mcp",json.dumps(mcp_config,indent=2,ensure_ascii=False))

async def main():
    async with Client(mcp_config) as client:
        tool_data=[]
        for tool in await client.list_tools():
            tool_data.append(tool.model_dump())

        print(json.dumps(tool_data))

        # Execute operations

        result = await LlmCallToolConverter(client).call_tool("get_traditional_indicators",
                                        {"full_symbol": "CRYPTO:GLOBAL:BTCUSD",
                                         "interval": "60M",
                                         "format": "CSV",
                                         "limit": 30,
                                         "is_eth": False,
                                         "indicators":["MA", "RSI", "MACD", "BOLL","ema"],
                                         "ma_periods":[5, 10, 20, 60]
                                         },

                                        )

        result = await LlmCallToolConverter(client).call_tool("get_traditional_indicators",
                                        {"full_symbol": "CRYPTO:GLOBAL:BTCUSD",
                                         "interval": "60M",
                                         "format": "CSV",
                                         "limit": 30,
                                         "is_eth": False,
                                         "indicators":["MA", "RSI", "MACD", "BOLL","ema"],
                                         "ma_periods":[5, 10, 20, 60]
                                         },)
        print(result)

asyncio.run(main())