from aitrados_api.common_lib.contant import ApiDataFormat, EventImpact
from fastmcp import FastMCP, Context
from pydantic import Field
from finance_trading_ai_agents_mcp.mcp_result_control.common_control import CommonControl
from finance_trading_ai_agents_mcp.utils.common_utils import mcp_get_api_params, show_mcp_result
from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance
mcp = FastMCP("economic_calendar")

mcp_app = mcp.http_app(path="/", transport="streamable-http", stateless_http=True)


@mcp.tool(title="Get economic calendar event codes")
async def get_economic_calendar_event_codes(context: Context,
                                            country_iso_code: str = Field(
                                                description="Country ISO code like US, CN, GB, JP"),
                                            ):
    """
    Get available economic calendar event codes for a specific country.
    Use this to find valid event_code values for other economic calendar functions.

    Args:
        country_iso_code: Two-letter ISO country code

    Returns:
        List of available event codes for the specified country
    """
    try:
        params = {
            "country_iso_code": country_iso_code,
        }
        empty_data_result = f"No event codes found"
        params = mcp_get_api_params(context, params)
        latest_events = await AitradosApiServiceInstance.api_client.economic.a_event_codes(**params)
        result=CommonControl(latest_events).result(empty_data_result=empty_data_result).mcp_result
        show_mcp_result(mcp,result)
        return result
    except Exception as e:
        result=f"{e}"
        show_mcp_result(mcp, result,True)
        return result


@mcp.tool(title="Get upcoming economic calendar events")
async def get_upcoming_economic_calendar_event_list(context: Context,
                                                    country_iso_code: str = Field(
                                                        description="Country ISO code like US, CN, GB, JP"),
                                                    event_code: str = Field(None,
                                                                            description="Economic event code. Use get_economic_calendar_event_codes to find valid codes"),
                                                    impact: str = Field(EventImpact.ALL,
                                                                        description=f"Impact level. Values: {EventImpact.get_array()}"),
                                                    format: str = Field(ApiDataFormat.CSV,
                                                                        description="Output format: csv or json"),
                                                    limit: int = Field(5, description="Number of events to return",
                                                                       ge=1, le=100),
                                                    ):
    """
    Get upcoming economic calendar events for a specific country.

    Args:
        country_iso_code: Two-letter ISO country code
        event_code: Specific event code (optional). Get codes from get_economic_calendar_event_codes
        impact: Filter by impact level (HIGH, MEDIUM, LOW, ALL)
        format: Data output format
        limit: Maximum number of events to return

    Returns:
        List of upcoming economic events
    """
    try:
        params = {
            "country_iso_code": country_iso_code,
            "event_code": event_code,
            "impact": impact,
            "date_type": "upcoming",
            "limit": limit,
            "format": format,
        }
        empty_data_result = f"No upcoming economic calendar events found"
        params = mcp_get_api_params(context, params)
        latest_events = await AitradosApiServiceInstance.api_client.economic.a_latest_events(**params)

        result=CommonControl(latest_events).result(empty_data_result=empty_data_result).mcp_result
        show_mcp_result(mcp,result)
        return result
    except Exception as e:
        result=f"{e}"
        show_mcp_result(mcp, result,True)
        return result


@mcp.tool(title="Get latest economic calendar events")
async def get_latest_economic_calendar_event_list(context: Context,
                                                  country_iso_code: str = Field(
                                                      description="Country ISO code like US, CN, GB, JP"),
                                                  event_code: str = Field(None,
                                                                          description="Economic event code. Use get_economic_calendar_event_codes to find valid codes"),
                                                  impact: str = Field(EventImpact.ALL,
                                                                      description=f"Impact level. Values: {EventImpact.get_array()}"),
                                                  format: str = Field(ApiDataFormat.CSV,
                                                                      description="Output format: csv or json"),
                                                  limit: int = Field(5, description="Number of events to return", ge=1,
                                                                     le=100),
                                                  ):
    """
    Get recent economic calendar events that have already occurred.

    Args:
        country_iso_code: Two-letter ISO country code
        event_code: Specific event code (optional). Get codes from get_economic_calendar_event_codes
        impact: Filter by impact level (HIGH, MEDIUM, LOW, ALL)
        format: Data output format
        limit: Maximum number of events to return

    Returns:
        List of recent economic events
    """
    try:
        params = {
            "country_iso_code": country_iso_code,
            "event_code": event_code,
            "impact": impact,
            "date_type": "historical",
            "limit": limit,
            "format": format,
        }
        empty_data_result = f"No recent economic calendar events found"
        params = mcp_get_api_params(context, params)
        latest_events = await AitradosApiServiceInstance.api_client.economic.a_latest_events(**params)
        result=CommonControl(latest_events).result(empty_data_result=empty_data_result).mcp_result
        show_mcp_result(mcp,result)
        return result

    except Exception as e:
        result=f"{e}"
        show_mcp_result(mcp, result,True)
        return result
