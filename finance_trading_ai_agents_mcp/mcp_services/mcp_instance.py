from contextlib import asynccontextmanager, AsyncExitStack
from fastapi import FastAPI
from finance_trading_ai_agents_mcp.mcp_services.economic_calendar_service import mcp_app as economic_calendar_mcp_app
from finance_trading_ai_agents_mcp.mcp_services.global_instance import CustomMcpServer
from finance_trading_ai_agents_mcp.mcp_services.http_service import set_mcp_config
from finance_trading_ai_agents_mcp.mcp_services.news_service import mcp_app as news_mcp_app
from finance_trading_ai_agents_mcp.mcp_services.price_action_service import mcp_app  as price_action_mcp_app
from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_service import mcp_app as traditional_indicator_mcp_app
from finance_trading_ai_agents_mcp.parameter_validator.analysis_departments import analysis_department


@asynccontextmanager
async def app_lifespan(app: FastAPI):

    print("Starting up the mcp app...")
    from aitrados_api.trade_middleware_service.trade_middleware_service_instance import AitradosApiServiceInstance
    if not AitradosApiServiceInstance.latest_ohlc_multi_timeframe_manager:
        from aitrados_api.universal_interface.aitrados_instance import ws_client_instance
    yield



    print("mcp server Stoped")




@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:

        await stack.enter_async_context(app_lifespan(app))
        await stack.enter_async_context(economic_calendar_mcp_app.lifespan(app))
        await stack.enter_async_context(traditional_indicator_mcp_app.lifespan(app))
        await stack.enter_async_context(price_action_mcp_app.lifespan(app))
        await stack.enter_async_context(news_mcp_app.lifespan(app))
        for custom_mcp_app in CustomMcpServer._mcp_apps:
            await stack.enter_async_context(custom_mcp_app.lifespan(app))
        yield


app = FastAPI(lifespan=combined_lifespan)
set_mcp_config(app)




app.mount("/traditional_indicator", traditional_indicator_mcp_app)
app.mount("/price_action", price_action_mcp_app)
app.mount("/economic_calendar", economic_calendar_mcp_app)
app.mount("/news", news_mcp_app)

def add_custom_mcp():
    for custom_mcp in  CustomMcpServer.mcp_list:
        server_name=custom_mcp.name or "unknown name"
        name_=server_name.replace(' ', '_').lower()
        name=name_.lower()
        #if  analysis_department.is_valid_department(name):
        #    continue
        custom_mcp_app=custom_mcp.http_app(path="/",transport="streamable-http",stateless_http=True)
        app.mount(f"/{name}", custom_mcp_app)
        analysis_department.add_department(name, server_name)
        CustomMcpServer._mcp_apps.append(custom_mcp_app)


add_custom_mcp()