---
title: "RPC & Subscriber Client Guide"
weight: 30
description: "How to use the AiTrados RPC frontend and the asynchronous subscriber to fetch latest OHLC chart flows and subscribe to middleware topics."
icon: "plug"
date: "2025-10-10T22:00:00+01:00"
lastmod: "2025-10-10T22:00:00+01:00"
draft: false
author: "VON"
tags: ["RPC", "Subscriber", "Pub/Sub", "OHLC", "Middleware", "ZeroMQ"]
categories: ["Middleware", "API"]
keywords: ["rpc client", "subscriber", "ohlc", "call_sync", "AsyncSubscriber"]
---

# RPC & Subscriber Client Guide

This page demonstrates two common client patterns when interacting with the AiTrados trading middleware:

- Synchronous RPC to obtain the latest OHLC chart flow or trigger an initial fetch.
- Asynchronous subscription to middleware topics (OHLC streams, news, events, and custom topics).

Both examples assume the middleware is already running (see Run Trading Middleware guide).

## Overview

- FrontendRequest.call_sync provides a convenient synchronous RPC for commands that must return immediately.
- AsyncSubscriber receives pub/sub messages from the middleware and routes them to async handlers.
- The middleware will automatically fetch and merge API + WebSocket data on the first request for a symbol/interval; subsequent pulls reuse the cached/streaming data.

## Quick start — Sync RPC (get latest OHLC / start chart flow)

Use this minimal pattern to request the latest OHLC chart flow or trigger the middleware to fetch and maintain the stream.

```python
# Example: synchronous RPC to get latest OHLC / start chart flow
# filepath: example_rpc_call.py
from aitrados_api.common_lib.any_list_data_to_format_data import any_data_to_format_data
from aitrados_api.common_lib.contant import IntervalName
from aitrados_api.trade_middleware.request import FrontendRequest
from aitrados_api.trade_middleware_service.trade_middleware_identity import aitrados_api_identity as idt
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    result = FrontendRequest.call_sync(
        idt.backend_identity,
        idt.fun.ADD_LATEST_OHLC_CHART_FLOW_ITEM_OR_GET_DATA,
        full_symbol="CRYPTO:GLOBAL:BTCUSD",
        interval=IntervalName.M15,
        timeout=70  # seconds
    )
    logger.info(f"request result: {result}")
    data = any_data_to_format_data(result)
    # ... use `data` (converted format) in your strategy ...
```

Notes:
- On first call for a (symbol, interval) pair the middleware will fetch missing historical data from the API and then join live WebSocket OHLC updates into a single continuous chart flow.
- Later calls for the same pair will return the latest merged data without re-calling the upstream API.

## Quick start — Async Subscriber (subscribe to topics)

Use AsyncSubscriber to receive all topic messages with dedicated async handlers. The class below shows common handler names used by the middleware.

```python
# Example: async subscriber skeleton
# filepath: example_subscriber.py
import time
from loguru import logger
from aitrados_api.common_lib.any_list_data_to_format_data import AnyListDataToFormatData, deserialize_multi_symbol_multi_timeframe_data
from aitrados_api.trade_middleware.request import AsyncFrontendRequest, FrontendRequest
from aitrados_api.trade_middleware.subscriber import AsyncSubscriber
from aitrados_api.trade_middleware_service.trade_middleware_identity import aitrados_api_identity as idt

class MyAsyncSubscriber(AsyncSubscriber):
    async def on_ohlc(self, msg):
        # stream of OHLC messages
        pass

    async def on_ohlc_chart_flow_streaming(self, msg):
        full_symbol = msg["full_symbol"]
        interval = msg["interval"]
        df = AnyListDataToFormatData(msg["data"]).get_polars()
        print("on_ohlc_chart_flow_streaming", full_symbol, interval)

    async def on_multi_symbol_multi_timeframe(self, msg):
        name = msg["name"]
        data = deserialize_multi_symbol_multi_timeframe_data(msg["data"], to_format="pandas")

    async def on_news(self, msg):
        print("on_news", msg)

    async def on_event(self, msg):
        print("on_event", AnyListDataToFormatData(msg).get_csv())

    async def on_show_subscribe(self, msg):
        all_subscribed_topics = await AsyncFrontendRequest.call_sync(idt.backend_identity, idt.fun.ALL_SUBSCRIBED_TOPICS)
        print("all_subscribed_topics", all_subscribed_topics)

if __name__ == "__main__":
    subscriber = MyAsyncSubscriber()
    subscriber.run()  # starts the async loop and connects to middleware
    # subscribe to topics (examples)
    subscriber.subscribe_topics("on_my_first_sub_topic")
    subscriber.subscribe_topics(*idt.channel.get_array())  # subscribe common channels

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("close...")
```

Integration tips:
- Use FrontendRequest.call_sync from the subscriber or other clients to request subscription changes (e.g., SUBSCRIBE_OHLC_1M).
- Subscriber handlers follow naming conventions (on_ohlc, on_news, on_event, on_ohlc_chart_flow_streaming, etc.). Add handlers you need in a subclass.

## Expected output (example logs)

A healthy middleware and client will produce logs similar to the runbook. Example client-side output when receiving chart flow streaming:

```
on_ohlc_chart_flow_streaming CRYPTO:GLOBAL:BTCUSD M15
on_news {'headline': '...'}
on_event <CSV of event>
request result: {...}
```

See the Run Trading Middleware page for router start logs and addresses.

## Instance reuse & multi-process guidance

- Clients should treat middleware-managed managers (api_client, ws_client, chart managers) as shared logical instances. Access them via RPC rather than creating local duplicates.
- For CPU-bound strategies avoid running them in the same process as the main middleware routers — Python's GIL can become a bottleneck.
- Recommended deployment:
  1. Middleware process: runs RPC & Pub/Sub routers, chart managers and clients.
  2. Worker processes: run heavy strategies (Python multiprocess, Rust/C++ services, or separate containers). Communicate via ZeroMQ-backed RPC/pub-sub.
- This pattern preserves single-source data and reduces redundant API calls.

## Best practices

- Use call_sync for short blocking requests and AsyncFrontendRequest for async captures in event handlers.
- Subscribe only to channels you need; middleware will reuse data streams efficiently across subscribers.
- Prefer worker processes for long-running tasks (LLM inference, heavy signal processing).

## Troubleshooting

- If you see no messages: verify middleware is running and check pub/sub and RPC addresses in middleware logs.
- IPC socket files in /tmp can persist between runs; remove stale socket files or restart the middleware gracefully.
- Enable DEBUG logging on both client and middleware to inspect registration and topic subscription flows.

## References

- Run Trading Middleware — startup and operational notes.
- Middleware identity module — available channels and RPC function names (aitrados_api_identity).
- Example scripts in the repository for run_trade_middleware and custom pub services.


