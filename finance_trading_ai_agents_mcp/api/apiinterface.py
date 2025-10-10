from aitrados_api import DatasetClient
from aitrados_api import WebSocketClient
from aitrados_api import LatestOhlcMultiTimeframeManager




class ApiInterface:
    def __init__(self):
        from finance_trading_ai_agents_mcp.api.api_instance import api_client, ws_client, \
            latest_ohlc_multi_timeframe_manager,timeframe_item_manager,callback_manage


        self.api_client:DatasetClient=api_client
        self.ws_client:WebSocketClient=ws_client
        self.timeframe_manager:LatestOhlcMultiTimeframeManager=latest_ohlc_multi_timeframe_manager
        self.callback_manage=callback_manage

        #self.ws_client.run(is_thread=True)

        self.timeframe_item_manager = timeframe_item_manager
        print("只初始化一次")


api_interface=ApiInterface()