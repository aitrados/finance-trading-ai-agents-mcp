import time

from aitrados_api.common_lib.common import is_debug
from fastmcp import FastMCP, Context


from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance
from finance_trading_ai_agents_mcp.mcp_result_control.common_control import CommonControl
from finance_trading_ai_agents_mcp.utils.common_utils import mcp_get_api_params, show_mcp_result

mcp = FastMCP("news")



mcp_app=mcp.http_app(path="/",transport="streamable-http",stateless_http=True)



@mcp.tool(title="Get latest news list")
async def get_latest_news_list(context: Context,
                               full_symbol: str,
                               limit: int = 5,
                               ):
    """
    :param full_symbol: Reference system prompt words
    :param limit: rows count.The number cannot be too large, otherwise it will affect the length of llm
    """
    try:
        params = {
            "full_symbol": full_symbol,
            "limit": limit,
        }
        params = mcp_get_api_params(context, params)
        ohlc_latest = await AitradosApiServiceInstance.api_client.news.a_news_latest(**params)

        result=CommonControl(ohlc_latest).result(empty_data_result="No recent news found.").mcp_result
        show_mcp_result(mcp,result)
        return result
    except Exception as e:
        result=f"{e}"
        show_mcp_result(mcp, result,True)
        return result

