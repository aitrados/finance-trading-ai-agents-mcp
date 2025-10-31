import datetime
from typing import List, Any
from fastmcp import Client
from fastmcp.client.progress import ProgressHandler
from mcp import Tool
from mcp.types import CallToolResult
from finance_trading_ai_agents_mcp.assistive_tools.aitrados_mcp_client import AitradosMcpClient
import asyncio

class McpListToolsConverter:
    def __init__(self,client: Client|AitradosMcpClient=None,list_tools:list[Tool]=None):
        self.list_tools =list_tools
        if not client and not list_tools:
            raise Exception("client or list_tools must be provided")


        if not list_tools and isinstance(client,AitradosMcpClient):
            self.client = client.client
        else:
            self.client = client


        self.base_result:List[dict]=[]

    async def __get_data(self):
        if not self.list_tools:


            self.list_tools: List[Tool] = await self.client.list_tools()

        for tool in self.list_tools:
            function_schema = {
                "name": tool.name,
                "title": tool.title,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
            item={"type": "function", "function": function_schema}
            self.base_result.append(item)

    async def get_result(self, output_type="list"):
        await self.__get_data()
        if output_type == "dict":
            result = {item["function"]["name"]: item for item in self.base_result}
            return result
        return self.base_result


class LlmCallToolConverter:
    def __init__(self,client: Client|AitradosMcpClient=None):
        if isinstance(client,AitradosMcpClient):
            self.client = client.client
        else:
            self.client = client



    async def __get_data(self,base_result:CallToolResult):
        result=""
        for content in base_result.content:
            if result:
                result+="\n"
            result+=content.text
        return result

    async def call_tool(self,  name: str,
                        arguments: dict[str, Any] | None = None,
                        timeout: datetime.timedelta | float | int | None = None,
                        progress_handler: ProgressHandler | None = None,
                        raise_on_error: bool = False):
        base_result = await self.client.call_tool(name,arguments,timeout,progress_handler,raise_on_error)

        return await self.__get_data(base_result)

    async def execute_tool_call(self,name,params:dict):
        return await self.call_tool(name, params)

    async def execute_langchain_tool_call(self,tool_calls:List[dict]):


        tool_tasks = [self.execute_tool_call(tc["name"],tc["args"]) for tc in tool_calls]
        tool_responses = await asyncio.gather(*tool_tasks)
        return tool_responses





