from aitrados_api.common_lib.contant import SubscribeEndpoint

from finance_trading_ai_agents_mcp import mcp_run
from finance_trading_ai_agents_mcp.api.apiinterface import api_interface



if __name__ == "__main__":
    api_interface.ws_client.init_data(SubscribeEndpoint.DELAYED),
    mcp_run()