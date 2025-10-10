
import uvicorn
import asyncio
from typing import Optional


from finance_trading_ai_agents_mcp.mcp_services.addition_custom_mcp_tool import add_addition_custom_mcp
def mcp_run(port: int = 11999, host: str = "127.0.0.1", addition_custom_mcp_py_file: Optional[str] = None):
    """
    Start MCP server

    Args:
        port: Server port
        host: Server host
        addition_custom_mcp_py_file: Custom MCP file path
    """
    # Load custom MCP
    add_addition_custom_mcp(addition_custom_mcp_py_file)

    config = uvicorn.Config(
        app="finance_trading_ai_agents_mcp.mcp_services.mcp_instance:app",
        host=host,
        port=port,
        reload=False
    )
    server = uvicorn.Server(config)
    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        from finance_trading_ai_agents_mcp.api.apiinterface import api_interface
        api_interface.api_client.close()
        api_interface.ws_client.close()
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
