import threading
from time import sleep

from aitrados_api.common_lib.response_format import UnifiedResponse
from aitrados_api.common_lib.tools.toml_manager import TomlManager
from loguru import logger




def auto_run_brokers(*broker_key):


    if not broker_key:
        auto_run_brokers=TomlManager.get_value("auto_run_brokers")
        if not auto_run_brokers:
            return None
    else:
        auto_run_brokers=broker_key

    #wait broker rpc and pub/sub service stared
    try:
       import aitrados_broker

    except ImportError:
        logger.error("load package aitrados_broker error: pip install aitrados-broker -U . Or config.toml set  auto_run_brokers=[]")
        exit()

    from aitrados_broker.run import run_broker_process
    from aitrados_broker.addition_custom_mcps.addition_broker_mcp_service import AdditionBrokerMcpService
    from aitrados_broker.trade_middleware_service.requests import broker_request
    from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService

    run_broker_process(is_thread=True)
    AdditionBrokerMcpService()


    def connect_broker():

        #waiting for starting broker rpc backend
        while True:
            sleep(1)
            try:
                result=UnifiedResponse(**broker_request('get_all_online_backend_services')).result
                if AitradosBrokerBackendService.IDENTITY.backend_identity in result:
                    break
            except :
                pass

        logger.debug(f"Auto connect brokers: {auto_run_brokers}")
        for broker in auto_run_brokers:
            broker_setting=TomlManager.get_value(f"broker.{broker}")
            if not broker_setting:
                logger.error(f"Broker '{broker}' .no found .please check config.toml \n"
                             f"auto_run_brokers=['your-broker-name']\n"
                             f"[broker.your-broker-name]")
                continue
            try:
                broker_request(AitradosBrokerBackendService.IDENTITY.fun.CONNECT, setting=broker_setting,broker_name=broker)
            except :
                logger.error(f"Broker '{broker}' Startup failed")
    threading.Thread(target=connect_broker,daemon=True).start()



