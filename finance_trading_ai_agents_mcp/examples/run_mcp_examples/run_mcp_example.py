from finance_trading_ai_agents_mcp import mcp_run
from finance_trading_ai_agents_mcp.examples.env_example import get_example_env
if __name__ == "__main__":
    get_example_env()
    mcp_run()
    #mcp_run(port=11999,host="127.0.0.1")



"""
modify subscription websocket server url
from finance_trading_ai_agents_mcp.api.apiinterface import api_interface
from aitrados_api.common_lib.contant import SubscribeEndpoint
api_interface.ws_client.init_data(SubscribeEndpoint.DELAYED),
"""