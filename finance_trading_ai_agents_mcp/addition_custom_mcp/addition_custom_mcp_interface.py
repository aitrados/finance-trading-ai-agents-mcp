import traceback
from abc import ABC

from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance
from fastmcp import FastMCP, Context

from aitrados_api.universal_interface.timeframe_item_management import TimeframeItemManager
from fastmcp.exceptions import NotFoundError

from finance_trading_ai_agents_mcp.mcp_services.global_instance import CustomMcpServer

'''
from fastmcp import Context

from finance_trading_ai_agents_mcp.mcp_services.economic_calendar_service import mcp as economic_calendar_mcp
from finance_trading_ai_agents_mcp.mcp_services.news_service import mcp as news_mcp
from finance_trading_ai_agents_mcp.mcp_services.price_action_service import mcp as price_action_mcp
from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_service import mcp as traditional_indicator_mcp
'''

class AdditionCustomMcpInterface(ABC):
    """
    Abstract base class for adding custom MCP (Model Context Protocol) tools.

    This interface allows you to extend the existing MCP services with custom functionality
    for economic calendar, news, price action, and traditional indicator analysis.

    Available API Access:
    - AitradosApiServiceInstance.api_client: REST API client for data retrieval
    - AitradosApiServiceInstance.ws_client: WebSocket client for real-time data streaming
    - AitradosApiServiceInstance.latest_ohlc_chart_flow_manager: ohlc chart flow roll
    - AitradosApiServiceInstance.latest_ohlc_multi_timeframe_manager Multi-timeframe OHLC data management
    - TimeframeItemManager: Timeframe item management utilities

    Usage:
        class MyCustomMcp(AdditionCustomMcpInterface):
            def custom_news_mcp(self):
                @news_mcp.tool(title="My Custom Tool")
                async def my_custom_function(context: Context, full_symbol: str = "STOCK:US:AAPL"):
                    # Access API data through AitradosApiServiceInstance
                    data = await AitradosApiServiceInstance.api_client.get_some_data()
                    return data
    """

    def __init__(self):
        self._initialize()
    def disable_tools(self,mcp:FastMCP,*function_name:str):
        #function_name is from examples/mcp_clients/**.py
        """
            await client.list_tools() and gain function name

        async with Client(mcp_config) as client:
        tool_data=[]
        for tool in await client.list_tools():
            tool_data.append(tool.model_dump())

        print(json.dumps(tool_data))
        """

        for name in function_name:
            try:
                mcp.add_tool()
                mcp.remove_tool(name)
            except Exception as e:
                if name=="function_name_to_remove":
                    continue

                raise ValueError(
                    """
                    #function_name is from examples/mcp_clients/**.py
                    
                    await client.list_tools() and gain function name
    
                    async with Client(mcp_config) as client:
                    tool_data=[]
                    for tool in await client.list_tools():
                        tool_data.append(tool.model_dump())
    
                    print(json.dumps(tool_data))
                    """
                )



    def _initialize(self):
        """Initialize all custom MCP tools"""
        try:
            self.custom_economic_calendar_mcp()
        except NotImplementedError:
            pass

        try:
            self.custom_news_mcp()
        except NotImplementedError:
            pass

        try:
            self.custom_price_action_mcp()
        except NotImplementedError:
            pass

        try:
            self.custom_traditional_indicator_mcp()
        except NotImplementedError:
            pass
        #add apartment
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name())
        except NotImplementedError:
            pass
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name1())
        except NotImplementedError:
            pass
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name2())
        except NotImplementedError:
            pass
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name3())
        except NotImplementedError:
            pass
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name4())
        except NotImplementedError:
            pass
        try:
            CustomMcpServer.add_mcp_server(self.add_mcp_server_name5())
        except NotImplementedError:
            pass

    def custom_economic_calendar_mcp(self):
        '''
        Economic calendar custom tool example:
        @economic_calendar_mcp.tool(title="Custom Economic Tool")
        async def get_custom_economic_data(context: Context, country_iso_code: str = "US"):
            return f"Custom economic data for {country_iso_code}"
        '''
        raise NotImplementedError("Please implement this method in the subclass")

    def custom_news_mcp(self):
        '''
        News service custom tool example:
        @news_mcp.tool(title="Custom News Tool")
        async def get_custom_news_data(context: Context, full_symbol: str = "STOCK:US:AAPL"):
            return f"Custom news data for {full_symbol}"
        '''
        raise NotImplementedError("Please implement this method in the subclass")

    def custom_price_action_mcp(self):
        '''
        Price action custom tool example:
        @price_action_mcp.tool(title="Custom Price Tool")
        async def get_custom_price_data(context: Context, full_symbol: str = "STOCK:US:AAPL", interval: str = "DAY"):
            return f"Custom price data for {full_symbol} on {interval}"
        '''
        raise NotImplementedError("Please implement this method in the subclass")

    def custom_traditional_indicator_mcp(self):
        '''
        Traditional indicator custom tool example:
        @traditional_indicator_mcp.tool(title="Custom Indicator Tool")
        async def get_custom_indicator_data(context: Context, full_symbol: str = "STOCK:US:AAPL", interval: str = "DAY"):
            return f"Custom indicator data for {full_symbol} on {interval}"
        '''
        raise NotImplementedError("Please implement this method in the subclass")

    def add_mcp_server_name(self)->FastMCP:
        '''
        ## http://127.0.0.1:11999/mcp_servers.json and see the custom_mcp_server1 server
        mcp = FastMCP("custom_mcp_server1")
        @mcp.tool(title="custom_mcp_server_name")
        async def get_custom_abc(context: Context, full_symbol: str = "STOCK:US:AAPL", interval: str = "DAY"):
            return f"Custom indicator data for {full_symbol} on {interval}"
        return mcp
        '''
        raise NotImplementedError("Please implement this method in the subclass")
    def add_mcp_server_name1(self)->FastMCP:
        #refer to self.add_mcp_server_name()
        raise NotImplementedError("Please implement this method in the subclass")
    def add_mcp_server_name2(self)->FastMCP:
        # refer to self.add_mcp_server_name()
        raise NotImplementedError("Please implement this method in the subclass")
    def add_mcp_server_name3(self)->FastMCP:
        # refer to self.add_mcp_server_name()
        raise NotImplementedError("Please implement this method in the subclass")
    def add_mcp_server_name4(self)->FastMCP:
        # refer to self.add_mcp_server_name()
        raise NotImplementedError("Please implement this method in the subclass")
    def add_mcp_server_name5(self)->FastMCP:
        # refer to self.add_mcp_server_name()
        raise NotImplementedError("Please implement this method in the subclass")