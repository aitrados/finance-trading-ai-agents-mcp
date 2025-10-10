import json
import os
import traceback
from typing import Dict, List, Callable
import pandas as pd
import polars as pl
from aitrados_api import SubscribeEndpoint, ChartDataFormat
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient
from aitrados_api import WebSocketClient
from aitrados_api import LatestOhlcMultiTimeframeManager
from aitrados_api.common_lib.common import is_debug
from loguru import logger

from finance_trading_ai_agents_mcp.api.timeframe_item_management import TimeframeItemManager
from finance_trading_ai_agents_mcp.utils.common_utils import get_env_value

timeframe_item_manager = TimeframeItemManager()
api_config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    debug=is_debug()
)


class CallbackManage:
    def __init__(self):
        self.__custom_multi_timeframe_callbacks: List[Callable] = []
        self.__custom_show_subscribe_handle_msgs: List[Callable] = []
        self.__custom_event_handle_msgs: List[Callable] = []
        self.__custom_news_handle_msgs: List[Callable] = []
        self.__custom_auth_handle_msgs: List[Callable] = []
        self.__custom_handle_msgs: List[Callable] = []
        self.__custom_ohlc_handle_msgs: List[Callable] = []

        self.__custom_ohlc_chart_flow_streaming_callbacks: List[Callable] = []





    def add_custom_multi_timeframe_callback(self, func):
        self.__custom_multi_timeframe_callbacks.append(func)
    def add_custom_ohlc_chart_flow_streaming_callback(self, func):
        self.__custom_ohlc_chart_flow_streaming_callbacks.append(func)

    def add_custom_show_subscribe_handle_msg(self, func):
        self.__custom_show_subscribe_handle_msgs.append(func)

    def add_custom_event_handle_msg(self, func):
        self.__custom_event_handle_msgs.append(func)

    def add_custom_news_handle_msg(self, func):
        self.__custom_news_handle_msgs.append(func)
    def add_custom_ohlc_handle_msg(self, func):
        self.__custom_ohlc_handle_msgs.append(func)
    def add_custom_auth_handle_msg(self, func):
        self.__custom_auth_handle_msgs.append(func)

    def add_custom_handle_msg(self, func):
        self.__custom_handle_msgs.append(func)

    def _default_multi_timeframe_callback(self, name, data: Dict[str, List[str | list | pl.DataFrame | pd.DataFrame]],
                                          **kwargs):
        timeframe_item_manager.receive_data(name, data)
        for cb in self.__custom_multi_timeframe_callbacks:
            try:
                cb(name, data)
            except Exception as e:
                traceback.print_exc()

    def _default_show_subscribe_handle_msg(self, client: WebSocketClient, message):
        for cb in self.__custom_show_subscribe_handle_msgs:
            try:
                cb(client, message)
            except Exception as e:
                traceback.print_exc()
    def _default_ohlc_chart_flow_streaming_callback(self, data):
        for cb in self.__custom_ohlc_chart_flow_streaming_callbacks:
            try:
                cb(data)
            except Exception as e:
                traceback.print_exc()


    def _default_event_handle_msg(self, client: WebSocketClient, data_list):
        """Default callback for handling event messages"""
        for cb in self.__custom_event_handle_msgs:
            try:
                cb(client, data_list)
            except Exception as e:
                logger.error(f"Error in custom event handler: {e}")
                traceback.print_exc()

    def _default_news_handle_msg(self, client: WebSocketClient, data_list):
        """Default callback for handling news messages"""
        for cb in self.__custom_news_handle_msgs:
            try:
                cb(client, data_list)
            except Exception as e:
                logger.error(f"Error in custom news handler: {e}")
                traceback.print_exc()
    def _default_ohlc_handle_msg(self, client: WebSocketClient, data_list):
        """Default callback for handling ohlc messages"""
        for cb in self.__custom_ohlc_handle_msgs:
            try:
                cb(client, data_list)
            except Exception as e:
                logger.error(f"Error in custom ohlc handler: {e}")
                traceback.print_exc()

    def _default_auth_handle_msg(self, client: WebSocketClient, message):
        """Default callback for handling authentication messages"""
        for cb in self.__custom_auth_handle_msgs:
            try:
                cb(client, message)
            except Exception as e:
                logger.error(f"Error in custom auth handler: {e}")
                traceback.print_exc()

    def _default_handle_msg(self, client: WebSocketClient, message):
        """Default callback for handling general messages"""

        for cb in self.__custom_handle_msgs:
            try:
                cb(client, message)
            except Exception as e:
                logger.error(f"Error in custom message handler: {e}")
                traceback.print_exc()
callback_manage=   CallbackManage()



api_client = DatasetClient(config=api_config)





ws_client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    is_reconnect=True,
    show_subscribe_handle_msg=callback_manage._default_show_subscribe_handle_msg,
    handle_msg=callback_manage._default_handle_msg,
    news_handle_msg=callback_manage._default_news_handle_msg,
    event_handle_msg=callback_manage._default_event_handle_msg,
    auth_handle_msg=callback_manage._default_auth_handle_msg,
    endpoint=SubscribeEndpoint.REALTIME,
    debug=is_debug()
)








latest_ohlc_multi_timeframe_manager = LatestOhlcMultiTimeframeManager(
    api_client=api_client,
    ws_client=ws_client,
    multi_timeframe_callback=callback_manage._default_multi_timeframe_callback,
    limit=get_env_value("LIVE_STREAMING_OHLC_LIMIT", 150),  # data length limit
    works=10,
    data_format=ChartDataFormat.POLARS,  # multi_timeframe_callback return data format
    latest_ohlc_chart_flow_callback=callback_manage._default_ohlc_chart_flow_streaming_callback
)

