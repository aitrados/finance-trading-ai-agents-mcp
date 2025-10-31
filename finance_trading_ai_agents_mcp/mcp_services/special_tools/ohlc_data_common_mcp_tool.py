import json
import re
import traceback
from copy import deepcopy
from typing import List, Union

from aitrados_api.common_lib.any_list_data_to_format_data import  AnyListDataToFormatData

from aitrados_api.common_lib.contant import ApiDataFormat
from aitrados_api.latest_ohlc_multi_timeframe_alignment_flow.unique_name_generator import UniqueNameGenerator
from fastmcp import FastMCP, Context
from pydantic import Field

from aitrados_api.universal_interface.timeframe_item_management import TimeframeItemManager
from finance_trading_ai_agents_mcp.mcp_result_control.common_control import CommonControl
from finance_trading_ai_agents_mcp.mcp_services.global_instance import McpGlobalVar
from finance_trading_ai_agents_mcp.utils.common_utils import split_full_symbol, mcp_get_api_params,show_mcp_result
from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance



class StreamingOhlcOperation:

    def __init__(self):
        pass
    def streaming_ohlc_to_llm_data(self,result:any,limit:int,format_:str):

        template="""
##### OHLC {full_symbol} -> {interval}
```{format_}
{content}
```
        """
        result_string = ""
        if not isinstance(result, dict):
            return result
        result = deepcopy(result)

        for full_symbol in list(result.keys()):
            for df in result[full_symbol]:
                interval = df["interval"][0]

                to_format = AnyListDataToFormatData(df,
                                                      rename_column_name_mapping=McpGlobalVar.rename_column_name_mapping(),
                                                      filter_column_names=McpGlobalVar.filter_column_names(), limit=limit)
                if format_ == "json":
                    string=json.dumps(to_format.get_list())
                else:
                    string = to_format.get_csv()
                    string = re.sub(r'\.000000\+', '+', string)
                result_string += template.format(full_symbol=full_symbol, interval=interval,format_=format_, content=string)

        return result_string


    async def get_result(self,item_data,limit,is_eth,format):



        original_name = UniqueNameGenerator.get_original_name(item_data=item_data, is_eth=is_eth)
        TimeframeItemManager.add_item(item_data=item_data, original_name=original_name, is_eth=is_eth)
        result = await TimeframeItemManager.aget_data_from_map(name=original_name,
                                                                               empty_data_result="Since no data was pulled, please stop the analysis and tell them to skip this analysis.")
        result = self.streaming_ohlc_to_llm_data(result, limit=limit,format_=format)

        return result



def ohlc_list_tool(mcp:FastMCP):

    @mcp.tool
    async def get_live_streaming_ohlc(context: Context,
                                   full_symbol: str,
                                   interval: str = "day",

                                   limit: int = Field(McpGlobalVar.default_ohlc_limit(), description="row number of results", ge=1, le=McpGlobalVar.live_streaming_ohlc_limit()),
                                   is_eth: bool = Field(False, description="Whether to include US stock extended hours data"),
                                      format: str = ApiDataFormat.CSV,
                                   ):
        try:
            mcp_get_api_params(context, {})
            item_data = {
                full_symbol: [interval],
            }
            result=await StreamingOhlcOperation().get_result(item_data=item_data,limit=limit,is_eth=is_eth,format=format)
            show_mcp_result(mcp, result)
            return result


        except Exception as e:
            traceback.print_exc()
            result = f"{e}"
            show_mcp_result(mcp, result, True)
            return result
    @mcp.tool
    async def get_multi_timeframe_live_streaming_ohlc(context: Context,
                                                      full_symbol: str,
                                                      intervals: Union[List[str]] = ["DAY"],
                                                        format: str = ApiDataFormat.CSV,
                                                        limit: int = Field(McpGlobalVar.default_ohlc_limit(), description="row number of results", ge=1, le=McpGlobalVar.live_streaming_ohlc_limit()),
                                                        is_eth: bool = Field(False, description="Whether to include US stock extended hours data"),
                                                      ):



        try:
            mcp_get_api_params(context, {})
            item_data = {
                full_symbol: intervals,
            }
            result=await StreamingOhlcOperation().get_result(item_data=item_data,limit=limit,is_eth=is_eth,format=format)

            show_mcp_result(mcp, result)
            return result


        except Exception as e:
            result = f"{e}"
            show_mcp_result(mcp, result, True)
            return result

    @mcp.tool
    async def get_multi_symbol_multi_timeframe_live_streaming_ohlc(context: Context,
                                                                   item_data:dict,
                                                                   format: str = ApiDataFormat.CSV,
                                                                   limit: int = Field(McpGlobalVar.default_ohlc_limit(), description="row number of results", ge=1, le=McpGlobalVar.live_streaming_ohlc_limit()),
                                                                   is_eth: bool = Field(False,
                                                                                        description="Whether to include US stock extended hours data"),
                                                                   ):
        try:
            mcp_get_api_params(context, {})
            result=await StreamingOhlcOperation().get_result(item_data=item_data,limit=limit,is_eth=is_eth,format=format)

            show_mcp_result(mcp, result)
            return result


        except Exception as e:
            result = f"{e}"
            show_mcp_result(mcp, result, True)
            return result

    @mcp.tool
    async def get_latest_ohlc(context: Context, full_symbol: str,
                                   interval: str = "DAY",
                                   format: str = ApiDataFormat.CSV,
                                   limit: int = Field(150, description="row number of results", ge=1, le=1000),
                                   is_eth: bool = Field(False, description="Whether to include US stock extended hours data"),
                                   ):
        """
        Get the latest OHLC data for a given financial instrument.

        :param full_symbol: Reference system prompt words
        :param interval: Reference system prompt words
        :param format: The desired output format (`csv` or `json`).
        :param limit: The number of data points to retrieve (1-1000).
        :param is_eth: Whether to include US stock extended hours data.
        :return: OHLC data in the specified format or other notice text.
        """

        try:
            schema_asset, country_symbol = split_full_symbol(full_symbol)

            params = {
                "schema_asset": schema_asset,
                "country_symbol": country_symbol,
                "interval": interval,
                "format": ApiDataFormat.CSV,
                "limit": limit,
                "is_eth": is_eth
            }
            params = mcp_get_api_params(context, params)
            ohlc_latest = await AitradosApiServiceInstance.api_client.ohlc.a_ohlcs_latest(**params)

            cc=CommonControl(ohlc_latest).result()
            result= cc.to_list_data(  rename_column_name_mapping=McpGlobalVar.rename_column_name_mapping(),  filter_column_names=McpGlobalVar.filter_column_names(),limit=limit,format=format)
            show_mcp_result(mcp, result)
            return result
        except Exception as e:
            result = f"{e}"
            show_mcp_result(mcp, result, True)
            return result


