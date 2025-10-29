from fastmcp import Client

from finance_trading_ai_agents_mcp.assistive_tools.assistive_tools_utils import get_client_mcp_config

class AitradosMcpClient:
    def __init__(self, departments: list[str]|str, mcp_base_url=None):
        self.mcp_config: dict = None
        self.mcp_base_url = mcp_base_url

        self.departments = departments if isinstance(departments,list) else [departments]
        self.client: Client = None
        self._client_context = None

    async def connect(self):
        if self.client is None:
            self.mcp_config = get_client_mcp_config(self.departments, mcp_base_url=self.mcp_base_url)
            self._client_context = Client(self.mcp_config)
            self.client = await self._client_context.__aenter__()
        return self.client

    async def disconnect(self):
        if self.client and self._client_context:
            await self._client_context.__aexit__(None, None, None)
            self.client = None
            self._client_context = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

'''
async def main():
    mcp_client = AitradosMcpClient(departments)

    try:
        await mcp_client.connect()
        # mcp_client.client
        result = await mcp_client.client.call_tool("tool_name", {})
    finally:
        await mcp_client.disconnect()

    # or
    async with AitradosMcpClient(departments) as mcp_client:
        result = await mcp_client.client.call_tool("tool_name", {})
'''