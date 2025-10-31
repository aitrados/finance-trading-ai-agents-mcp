import asyncio
import json

from aitrados_api.common_lib.contant import IntervalName
from fastmcp import Client

from finance_trading_ai_agents_mcp import analysis_department

from finance_trading_ai_agents_mcp.assistive_tools.assistive_tools_utils import get_client_mcp_config
from finance_trading_ai_agents_mcp.assistive_tools.mcp_tools_converter import LlmCallToolConverter

departments=[
 analysis_department.PRICE_ACTION
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
        result = await LlmCallToolConverter(client).call_tool("get_latest_ohlc",
                                        {"full_symbol": "STOCK:US:AAPL", "interval": "DAY", "format": "CSV",
                                         "limit": 150, "is_eth": False})
        print(result)

        result = await LlmCallToolConverter(client).call_tool("get_multi_timeframe_live_streaming_ohlc",
                                        {"full_symbol": "CRYPTO:GLOBAL:BTCUSD", "intervals": ["5m", "day"]})
        print(result)


        result = await LlmCallToolConverter(client).call_tool("get_live_streaming_ohlc",
                                        {"full_symbol": "CRYPTO:GLOBAL:BTCUSD", "interval": "day"})
        print(result)




        result2 = await LlmCallToolConverter(client).call_tool("get_multi_timeframe_live_streaming_ohlc",
                                         {"full_symbol": "CRYPTO:GLOBAL:BTCUSD", "intervals": ["day"]})
        print(result2)

        item_data = {
            "STOCK:US:AAPL": [IntervalName.DAY, IntervalName.M15, IntervalName.M60],
            "STOCK:US:TSLA": [IntervalName.DAY, IntervalName.M15, IntervalName.M60],

        }

        result3 = await LlmCallToolConverter(client).call_tool("get_multi_symbol_multi_timeframe_live_streaming_ohlc",
                                         {"item_data": item_data})

        print(result3)
asyncio.run(main())