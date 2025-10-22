---
title: "Custom Pub/Sub Service"
weight: 50
description: "Defines how to implement and register a custom pub/sub service inside your Go or JS module. Includes examples for using the AiTrados RPC frontend and the asynchronous subscriber to fetch latest OHLC chart flows and subscribe to middleware topics."
icon: "plug"
date: "2025-10-22T12:00:00+01:00"
lastmod: "2025-10-22T12:00:00+01:00"
draft: false
author: "VON"
tags: ["RPC", "Subscriber", "Pub/Sub", "OHLC", "Middleware", "ZeroMQ", "pub service", "module"]
categories: ["Middleware", "API"]
keywords: ["rpc client", "subscriber", "ohlc", "call_sync", "AsyncSubscriber", "pub service", "module"]
---

examples/trade_middleware_example/custom_pubsub_service_example.py
```python
import threading
import time

from aitrados_api.trade_middleware.publisher import async_publisher_instance
"""
at first ,run "python run_trade_middleware_example.py"
"""


test_sub_topic="on_my_first_sub_topic"
def publish_service_example():
    i = 0

    while True:

        msg = f"Hello {i} {time.time()}".encode()
        async_publisher_instance.send_topic(test_sub_topic,msg)
        i += 1
        time.sleep(2)

def subscriber_client_example():
    from aitrados_api.trade_middleware.subscriber import AsyncSubscriber
    class MyAsyncSubscriber(AsyncSubscriber):
        """
        Asynchronous function callback
        """

        async def on_my_first_sub_topic(self, msg):
            # my_first_sub_topic is from custom_pub_service_example.py
            print(test_sub_topic, msg)
            pass

    subscriber = MyAsyncSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(test_sub_topic)

if __name__ == "__main__":
    threading.Thread(target=publish_service_example, daemon=True).start()

    subscriber_client_example()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("close...")



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