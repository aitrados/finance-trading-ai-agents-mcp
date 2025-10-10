from finance_trading_ai_agents_mcp import RemoteCurl
def get_client_mcp_config(departments: list[str],mcp_base_url="http://127.0.0.1:11999") -> dict:
    """
    '''
    mcp_config={
      "mcpServers": {
        "news": {
          "url": "http://127.0.0.1:11999/news/",
          "transport": "streamable-http",
          "headers": {
            "SECRET_KEY": "xxx"
          }
        }
      }
    }
    '''
    """
    url=mcp_base_url+"/mcp.json"
    try:
        mcp_config = RemoteCurl.post(url, {"departments": departments})
        if not isinstance( mcp_config,dict) or "data" not in mcp_config:
            raise KeyError(mcp_config)
        return mcp_config["data"]
    except Exception as e:
        raise KeyError(f"Error requesting MCP configuration: {e}")


