import time
import traceback

from typing import List

from aitrados_api.common_lib.contant import ApiDataFormat
from fastmcp import FastMCP, Context
from pydantic import Field

from finance_trading_ai_agents_mcp.api.apiinterface import api_interface
from finance_trading_ai_agents_mcp.live_streaming_ohlc_operations.live_streaming_ohlc_operation import \
    LiveStreamingOriginalOhlcOperation

from finance_trading_ai_agents_mcp.mcp_services.global_instance import default_ohlc_limit
from finance_trading_ai_agents_mcp.mcp_services.special_tools.ohlc_data_common_mcp_tool import ohlc_list_tool
from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_operations.traditional_indicator_ops import \
    TraditionalIndicatorOps
from finance_trading_ai_agents_mcp.utils.common_utils import get_env_value, mcp_get_api_params, show_mcp_result

mcp = FastMCP("Traditional indicators")
ohlc_list_tool(mcp)

mcp_app=mcp.http_app(path="/",transport="streamable-http",stateless_http=True)

@mcp.tool(title="Get traditional indicators with OHLC data")
async def get_traditional_indicators(context: Context,
                                     full_symbol: str = Field(
                                         description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
                                     interval: str = Field("DAY",
                                                           description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
                                     indicators: List[str] = Field(["MA", "RSI", "MACD", "BOLL"],
                                                                   description="List of technical indicators",
                                                                   min_length=1, max_length=4),
                                     ma_periods: List[int] = Field([5, 10, 20, 60],
                                                                   description="Moving average periods", min_length=1,
                                                                   max_length=10),
                                     limit: int = Field(default_ohlc_limit, description="Number of rows to return",
                                                        ge=1, le=150),
                                     format: str = Field(ApiDataFormat.CSV, description="Output format: csv or json"),
                                     is_eth: bool = Field(False, description="Include US stock extended hours data"),
                                     ):
    """
    Get traditional technical indicators with OHLC data including Moving Average (MA),
    Relative Strength Index (RSI), MACD, and Bollinger Bands (BOLL).

    Args:
        full_symbol: Complete symbol format: asset_type:country:symbol
        interval: Candlestick time period
        indicators: Technical indicators to calculate
        ma_periods: Period parameters for moving averages
        limit: Number of data points to return
        format: Data output format
        is_eth: Include extended trading hours data

    Returns:
        Formatted data containing OHLC and technical indicators
    """
    try:
        mcp_get_api_params(context, {})
        item_data = {
            full_symbol: [interval],
        }
        ohlc_data=await LiveStreamingOriginalOhlcOperation().get_original_result(item_data=item_data,is_eth=is_eth)

        ohlc_data, added_columns = TraditionalIndicatorOps(ohlc_data, indicators, ma_periods).get_result()
        ohlc_data=LiveStreamingOriginalOhlcOperation.filter_ohlc_data_df(ohlc_data, added_columns)

        result=LiveStreamingOriginalOhlcOperation.get_llm_data(ohlc_data,format)
        show_mcp_result(mcp, result)
        return result




    except Exception as e:
        result=f"{e}"
        show_mcp_result(mcp, result,True)
        return result
