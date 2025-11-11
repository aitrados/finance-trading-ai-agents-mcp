import asyncio
import json

from aitrados_api.common_lib.contant import IntervalName
from fastmcp import Client

from aitrados_broker.addition_custom_mcps.parameter_validator.send_order_params import OffsetEnum, DirectionEnum, \
    OrderTypeEnum
from finance_trading_ai_agents_mcp import analysis_department

from finance_trading_ai_agents_mcp.assistive_tools.assistive_tools_utils import get_client_mcp_config
from finance_trading_ai_agents_mcp.assistive_tools.mcp_tools_converter import LlmCallToolConverter

departments=[
 analysis_department.BROKER
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


        print(await LlmCallToolConverter(client).call_tool("get_trading_account_summary",{"broker_name":None}))

        return
        cancel_order_data={
            #"order_id": "251109181143000002",
            "full_symbol_or_broker_symbol": "CRYPTO:GLOBAL:ETHUSD",
            "broker_name": None
        }
        print(await LlmCallToolConverter(client).call_tool("cancel_order", cancel_order_data))
        return
        send_order_data={
            "full_symbol_or_broker_symbol":"BTC-USDT-SWAP",#CRYPTO:GLOBAL:BTCUSD  "ETH-USDT-SWAP"
            "type":OrderTypeEnum.LIMIT,
            "volume":0.01,
            "price":2800,
            "offset":OffsetEnum.OPEN,
            "direction":DirectionEnum.LONG,
             "broker_name": None

        }

        print(await LlmCallToolConverter(client).call_tool("send_order",send_order_data))



asyncio.run(main())