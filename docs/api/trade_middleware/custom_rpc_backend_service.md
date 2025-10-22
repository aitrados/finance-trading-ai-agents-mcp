---
title: "Custom RPC Backend Service"
weight: 40
description: "Provides a backend service for remote RPC clients. Includes examples for implementing and registering RPC handlers in Go and JavaScript, and how to expose middleware endpoints."
icon: "server"
date: "2025-10-22T12:00:00+01:00"
lastmod: "2025-10-22T12:00:00+01:00"
draft: false
author: "VON"
tags: ["RPC", "Backend", "remote-rpc", "go", "javascript", "middleware"]
categories: ["Middleware", "API"]
keywords: ["rpc backend", "remote rpc", "go", "javascript", "rpc handlers", "middleware"]
---
examples/trade_middleware_example/custom_rpc_backend_service_example.py
```python
import threading
import time

from aitrados_api.common_lib.common import run_asynchronous_function
from aitrados_api.common_lib.response_format import ErrorResponse, UnifiedResponse
from aitrados_api.trade_middleware.backend_service import BackendService
from aitrados_api.trade_middleware.request import FrontendRequest

from examples.trade_middleware_example.custom_identity_example import my_custom_identity_example
from aitrados_api.trade_middleware.response import AsyncBackendResponse
"""
at first ,run "python run_trade_middleware_example.py"
"""
class CustomRpcBackendService(BackendService):
    IDENTITY=my_custom_identity_example
    def __init__(self):
        super().__init__()
    def last_ohlc_price_row(self,*args,**kwargs):

        # you can get other rpc data
        """
        from aitrados_api.common_lib.contant import SchemaAsset, IntervalName
        from aitrados_api.trade_middleware.request import FrontendRequest,AsyncFrontendRequest
        from aitrados_api.trade_middleware_service.trade_middleware_identity import aitrados_api_identity
        params = {
            "schema_asset": SchemaAsset.CRYPTO,
            "country_symbol": "GLOBAL:BTCUSD",
            "interval": IntervalName.M60,
            "limit": 1
        }
        ohlcs = FrontendRequest.call_sync(
            aitrados_api_identity.backend_identity,
            aitrados_api_identity.fun.OHLCS,
            **params,
        )
        """
        return UnifiedResponse(result="price is 456").model_dump_json()
    def first_ohlc_price_row(self,*args,**kwargs):

        return UnifiedResponse(result="price is 789").model_dump_json()


    def accept(self,function_name:str,*args,**kwargs):
        if function_name==my_custom_identity_example.fun.FIRST_OHLC_PRICE_ROW.value:
            return self.first_ohlc_price_row(*args,**kwargs)
        if function_name==my_custom_identity_example.fun.LAST_OHLC_PRICE_ROW.value:
            return self.last_ohlc_price_row(*args,**kwargs)
        else:
            return ErrorResponse(message=F"Unknown request '{function_name}'").model_dump_json()

    async def a_accept(self,function_name:str,*args,**kwargs):
        if function_name not in my_custom_identity_example.fun.get_array():
            return ErrorResponse(message=F"Unknown request '{function_name}'").model_dump_json()
        #to sync function.If the concurrency is high, we recommend using asynchronous functions
        return self.accept(function_name,*args,**kwargs)


def run_service():

    service = AsyncBackendResponse(CustomRpcBackendService())
    run_asynchronous_function(service.init())


def test_request():
    print("test req")
    result = FrontendRequest.call_sync(
        CustomRpcBackendService.IDENTITY.backend_identity,
        CustomRpcBackendService.IDENTITY.fun.LAST_OHLC_PRICE_ROW,
        full_symbol="CRYPTO:GLOBAL:BTCUSD",
        timeout=30  # 10s
    )
    print(result)
if __name__ == "__main__":
    #run rpc backend
    router_thread = threading.Thread(target=run_service, daemon = True).start()

    time.sleep(5)
    #request
    test_request()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("closing...")




```



examples/trade_middleware_example/custom_identity_example.py
```python
from aitrados_api.trade_middleware.identity_mixin import *
class RpcFunction(RpcFunctionMixin):
    LAST_OHLC_PRICE_ROW = "last_ohlc_price_row"
    FIRST_OHLC_PRICE_ROW = "first_ohlc_price_row"
class Channel(ChannelMixin):
    MY_TEST_SUB = b"my_test_sub"
    MY_SECOND_SUB = b"my_second_sub"
class Identity(IdentityMixin):
    backend_identity = "my_first_package"
    fun = RpcFunction
    channel = Channel
my_custom_identity_example=Identity


```