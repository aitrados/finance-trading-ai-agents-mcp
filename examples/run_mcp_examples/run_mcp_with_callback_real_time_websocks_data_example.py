
from aitrados_api.universal_interface.callback_manage import CallbackManage
from finance_trading_ai_agents_mcp import mcp_run


"""
Real-time WebSocket Data Integration with MCP Server

This script demonstrates how to run an MCP (Model Context Protocol) server while simultaneously 
receiving real-time WebSocket data streams, achieving data reusability across your project.

Key Benefits:

🔄 **Data Reusability**: 
   - The same real-time data feed serves both MCP clients (like Claude Desktop) and your custom application logic
   - Eliminates duplicate API calls and reduces bandwidth usage
   - Centralizes data management in one location

⚡ **Real-time Integration**:
   - Multi-timeframe OHLC data: Real-time price feeds for trading analysis
   - Event data: Market events, earnings, splits, etc.
   - News data: Financial news updates as they happen
   - Authentication: Connection status and auth events
   - General messages: System notifications and other data

🏗️ **Architecture Advantages**:
   - MCP server handles AI/LLM requests with structured financial data
   - Custom callbacks process the same data for your trading algorithms
   - WebSocket connection is shared, ensuring data consistency
   - Thread-safe data management with proper synchronization

📊 **Use Cases**:
   - AI-powered trading assistants with real-time market data
   - Automated trading systems with LLM decision support
   - Real-time portfolio monitoring with AI analysis
   - Market research tools combining AI insights with live data
   - Risk management systems with instant alert capabilities

🎯 **Practical Example**:
   When Claude Desktop requests "Show me AAPL's current price", the MCP server provides real-time data.
   Simultaneously, your custom callback can execute trading logic based on the same price update.
   This eliminates the need for separate data feeds and ensures perfect synchronization.

⚙️ **Callback System**:
   Each callback type handles specific data streams:
   - multi_timeframe_callback: OHLC candlestick data for technical analysis
   - event_handle_callback: Corporate actions and market events
   - news_handle_callback: Breaking financial news
   - auth_handle_callback: Connection and authentication status
   - general_handle_callback: System messages and notifications
   - show_subscribe_handle_callback: Subscription management events

This dual-purpose architecture maximizes the value of your real-time data subscription while 
providing both AI capabilities and custom application logic in a single, efficient system.
"""


def multi_timeframe_callback(*args,**kwargs):
    print("Multi-timeframe data received:", args,kwargs)


def event_handle_callback(client, *args,**kwargs):
    print("Event data received:", args,kwargs)


def news_handle_callback(client, *args,**kwargs):
    print("News data received:", args,kwargs)


def auth_handle_callback(client, *args,**kwargs):
    print("Auth message received:", args,kwargs)


def general_handle_callback(client, *args,**kwargs):
    print("General message received:", args,kwargs)


def show_subscribe_handle_callback(client, *args,**kwargs):
    print("Subscribe handle message received:", args,kwargs)


def ohlc_chart_flow_streaming_callback(*args,**kwargs):
    print("OHLC chart flow streaming data received:", args,kwargs)


def ohlc_handle_callback(client, *args,**kwargs):
    print("OHLC handle message received:", args,kwargs)
def error_handle_callback(client, *args,**kwargs):
    print("Error handle message received:", args,kwargs)


if __name__ == "__main__":
    #from examples.env_example import get_example_env
    #get_example_env()
    #from aitrados_api.common_lib.common import load_env_file
    #load_env_file(file=None, override=True)
    # Register all custom callbacks
    CallbackManage.add_custom_multi_timeframe_callback(multi_timeframe_callback)
    CallbackManage.add_custom_event_handle_msg(event_handle_callback)
    CallbackManage.add_custom_news_handle_msg(news_handle_callback)
    CallbackManage.add_custom_auth_handle_msg(auth_handle_callback)
    CallbackManage.add_custom_handle_msg(general_handle_callback)
    CallbackManage.add_custom_show_subscribe_handle_msg(show_subscribe_handle_callback)

    CallbackManage.add_custom_ohlc_chart_flow_streaming_callback(ohlc_chart_flow_streaming_callback)
    CallbackManage.add_custom_ohlc_handle_msg(ohlc_handle_callback)
    CallbackManage.add_custom_error_msgs(error_handle_callback)


    mcp_run()