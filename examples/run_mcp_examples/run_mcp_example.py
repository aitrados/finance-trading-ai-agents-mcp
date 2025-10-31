

from finance_trading_ai_agents_mcp import mcp_run



if __name__ == "__main__":
    #from aitrados_api.common_lib.common import load_env_file
    #from examples.env_example import get_example_env
    #get_example_env()
    #load_env_file(file=None,override=True)
    mcp_run()
    #mcp_run(port=11999,host="127.0.0.1")



"""
load_env_file(file=None,override=True)
modify subscription websocket server url
from aitrados_api.universal_interface.aitrados_instance import ws_client_instance
from aitrados_api.common_lib.contant import SubscribeEndpoint
ws_client_instance.init_data(SubscribeEndpoint.DELAYED)
"""

