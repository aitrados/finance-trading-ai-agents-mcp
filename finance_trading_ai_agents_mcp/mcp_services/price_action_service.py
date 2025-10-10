from fastmcp import FastMCP

from finance_trading_ai_agents_mcp.mcp_services.special_tools.ohlc_data_common_mcp_tool import ohlc_list_tool

mcp = FastMCP("price_action")

ohlc_list_tool(mcp)



mcp_app=mcp.http_app(path="/",transport="streamable-http",stateless_http=True)
