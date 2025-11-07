import asyncio
import json

from fastmcp import Client

from finance_trading_ai_agents_mcp import analysis_department
from finance_trading_ai_agents_mcp.assistive_tools.assistive_tools_utils import get_client_mcp_config
from finance_trading_ai_agents_mcp.assistive_tools.mcp_tools_converter import LlmCallToolConverter


departments=[
 analysis_department.ECONOMIC_CALENDAR
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


        result = await LlmCallToolConverter(client).call_tool("get_latest_economic_calendar_event_list", {"country_iso_code": "us","event_code":"EMPLOYMENT_INITIAL_JOBLESS_CLAIMS"})

        print(result)
asyncio.run(main())