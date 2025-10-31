import json
import re
from aitrados_api.common_lib.any_list_data_to_format_data import AnyListDataToFormatData
from aitrados_api.common_lib.common import to_format_data
from aitrados_api.latest_ohlc_multi_timeframe_alignment_flow.unique_name_generator import UniqueNameGenerator
from aitrados_api.universal_interface.timeframe_item_management import TimeframeItemManager


from finance_trading_ai_agents_mcp.mcp_services.global_instance import McpGlobalVar

class LiveStreamingOriginalOhlcOperation:
    def __init__(self):
        self.result=None

    def __get_original_streaming_ohlc_data(self, ohlc_data: any):
        if not isinstance(ohlc_data, dict):
            raise KeyError(ohlc_data)
        new_data={}
        for full_symbol in list(ohlc_data.keys()):

            new_data[full_symbol]=[]
            for i, df in enumerate(ohlc_data[full_symbol]):
                new_data[full_symbol].append(df.clone())


        return new_data

    async def get_original_result(self, item_data,  is_eth):

        name = UniqueNameGenerator.get_original_name(item_data=item_data, is_eth=is_eth)
        TimeframeItemManager.add_item(item_data=item_data, name=name, is_eth=is_eth)
        result = await TimeframeItemManager.aget_data_from_map(name=name,
                                                                               empty_data_result="Since no data was pulled, please stop the analysis and tell them to skip this analysis.")
        self.result = self.__get_original_streaming_ohlc_data(result)

        return self.result
    @staticmethod
    def filter_ohlc_data_df( ohlc_data:dict,preserve_columns=[]):
        for full_symbol in list(ohlc_data.keys()):
            for i, df in enumerate(ohlc_data[full_symbol]):
                filter_column_names_=McpGlobalVar.filter_column_names().copy()
                filter_column_names_.extend(preserve_columns)

                modified_df =  AnyListDataToFormatData(df,
                                                    rename_column_name_mapping=McpGlobalVar.rename_column_name_mapping(),
                                                    filter_column_names=filter_column_names_, limit=McpGlobalVar.default_ohlc_limit()).get_polars()
                ohlc_data[full_symbol][i] = modified_df
        return ohlc_data

    @staticmethod
    def get_llm_data(ohlc_data:dict,format="csv"):
        format=format.lower()
        if format=="json":
            format="dict"
        template = """##### full_symbol:{full_symbol}  interval:{interval}
```{format_}
{content}
```"""
        interval_key="interval"
        if McpGlobalVar.rename_column_name_mapping() and interval_key in McpGlobalVar.rename_column_name_mapping():
            interval_key=McpGlobalVar.rename_column_name_mapping()[interval_key]

        result_string = ""
        for full_symbol in list(ohlc_data.keys()):
            for df in ohlc_data[full_symbol]:


                interval = df[interval_key][0]

                df=AnyListDataToFormatData._get_formatted_float_column_df(df)

                content=to_format_data(df,format,is_copy=False)
                if format=="dict":
                    content=json.dumps(content)
                string = re.sub(r'\.000000\+', '+', content)
                result_string += template.format(full_symbol=full_symbol, interval=interval, format_=format,
                                                 content=string)

        return result_string



