
import json
from threading import RLock
from typing import TYPE_CHECKING, Dict, List
import polars as pl
import pandas as pd
from aitrados_api.common_lib.contant import IntervalName

from finance_trading_ai_agents_mcp.utils.common_utils import split_full_symbol, get_fixed_full_symbol, \
    get_real_intervals

if TYPE_CHECKING:
    from finance_trading_ai_agents_mcp.api.apiinterface import api_interface
import asyncio

class TimeframeItemManager:
    def __init__(self):

        self._api_interface=None
        self._lock = RLock()

        self.data_map={}

    async def aget_data_from_map(self, name, timeout=70,empty_data_result="Fetching data timeout: Failed to fetch data"):


        start_time = asyncio.get_event_loop().time()

        while True:
            # Use lock to safely read data
            with self._lock:
                if name in self.data_map and self.data_map[name] is not None:
                    return self.data_map[name]

            # Check if timeout occurred
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time >= timeout:
                raise TimeoutError(empty_data_result)

            # Wait 1 second before retry
            await asyncio.sleep(1)

    def __init_api_interface(self):
        from finance_trading_ai_agents_mcp.api.apiinterface import api_interface
        self._api_interface:api_interface=api_interface
    def receive_data(self,name, data: Dict[str, List[str | list | pl.DataFrame | pd.DataFrame]]):
        with self._lock:
            self.data_map[name]=data
        pass

    def add_item(self, item_data: dict, name=None, is_eth=False):
        with self._lock:
            name=self.get_name(item_data,name,is_eth)

            if name in self.data_map:
                return "subscribed"

            if not self._api_interface:
                self.__init_api_interface()
            self.data_map[name]=None
            self._api_interface.timeframe_manager.add_item(item_data=item_data,name=name,is_eth=is_eth)
            #print("data_map_keys",self.data_map.keys())
            return "subscribing"


    def get_name(self,item_data: dict, name=None, is_eth=False):
        item_data = self.__get_new_item_data(item_data)
        if not name:

            data = {
                "item_data": item_data,
                "is_eth": is_eth
            }
            name = json.dumps(data)
        return name

    def __get_fix_full_symbol_item_data(self, item_data: dict) -> dict:
        """
        Convert all full_symbol keys in item_data to unified format
        """
        fixed_item_data = {}

        for full_symbol, intervals in item_data.items():
            fixed_item_data[get_fixed_full_symbol(full_symbol)] = intervals


        return fixed_item_data

    def __get_new_item_data(self, item_data: dict) -> dict:
        """
        Reorder item_data
        1. Sort dictionary keys consistently (lexicographic order)
        2. Sort interval list for each symbol according to IntervalName.get_array() order
        """


        if not item_data:
            raise ValueError(f"Error: Missing item_data")

        item_data=self.__get_fix_full_symbol_item_data(item_data)

        # 1. Sort dictionary keys (ensure order consistency)
        sorted_keys = sorted(item_data.keys())

        # 2. Get interval sorting order
        sort_order = IntervalName.get_array()
        sort_key_map = {interval: i for i, interval in enumerate(sort_order)}

        # 3. Build new sorted dictionary
        new_item_data = {}

        for key in sorted_keys:
            intervals = item_data[key]
            if not intervals:
                new_item_data[key] = []
                raise ValueError(f"Error:{key} Missing interval")
                #continue
            intervals=get_real_intervals(intervals)

            # Sort interval list
            sorted_intervals = sorted(
                intervals,
                key=lambda interval: sort_key_map.get(interval, len(sort_order))
            )

            new_item_data[key] = sorted_intervals

        return new_item_data