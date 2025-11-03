import os
import traceback

import uvicorn
import asyncio
from typing import Optional

from aitrados_api.common_lib.common import get_env_bool_value, load_env_file
from finance_trading_ai_agents_mcp.mcp_services.addition_custom_mcp_tool import add_addition_custom_mcp
def mcp_run(port: int = 11999, host: str = "127.0.0.1", addition_custom_mcp_py_file: Optional[str] = None):
    """
    Start MCP server

    Args:
        port: Server port
        host: Server host
        addition_custom_mcp_py_file: Custom MCP file path
    """
    if not os.getenv('AITRADOS_SECRET_KEY') or os.getenv('AITRADOS_SECRET_KEY')=='YOUR_SECRET_KEY':
        load_env_file(override=True)
    if get_env_bool_value("ENABLE_RPC_PUBSUB_SERVICE"):
        from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
        AitradosTradeMiddlewareInstance.run_all()
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
        try:
            from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance

            AitradosApiServiceInstance.ws_client.close()
            AitradosApiServiceInstance.api_client.close()
        except:
            pass

        print("Server stopped by user")
    except Exception as e:
        traceback.print_exc()
        print(f"Server error: {e}")
