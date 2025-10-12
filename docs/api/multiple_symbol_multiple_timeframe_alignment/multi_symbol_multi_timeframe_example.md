---
weight: 30
date: "2025-09-16T00:00:00+01:00"
draft: false
author: "VON"
title: "MSMTF Implementation Guide and Examples"
toc: true
description: "Learn how to implement Multi-Symbol, Multi-Timeframe (MSMTF) alignment in your trading systems using our advanced OHLC API. This guide provides practical examples and code snippets to help you build sophisticated cross-market, multi-timeframe trading strategies."
publishdate: "2025-09-16T00:00:00+01:00"
tags: ["MSMTF Implementation", "API Examples", "Multi-Timeframe Alignment", "Trading Systems", "Real-time Data", "OHLC API"]
---

# Multi-Symbol, Multi-Timeframe Alignment

## Introduction

After exploring the theoretical foundations of [MTF Analysis](../multi_timeframe_overview/) and [MSMTF Analysis](../multi_symbol_multi_timeframe_overview/), this guide will demonstrate how to implement these powerful concepts using our OHLC API.

The MSMTF Alignment feature enables you to:

- **Synchronize data** across multiple assets and multiple timeframes
- **Process market data holistically** to identify cross-market patterns
- **Develop sophisticated strategies** that capitalize on inter-market relationships
- **Automate complex decision-making** based on multi-dimensional market analysis

## Getting Started with MSMTF Alignment

Our `LatestOhlcMultiTimeframeManager` class provides a powerful, flexible interface for working with multi-symbol, multi-timeframe data. This manager handles all the complex synchronization and alignment work behind the scenes, so you can focus on your trading logic.

### Prerequisites

- A valid AITRADOS API key [Quickstart](../../quickstart/)
- Basic understanding of Python and asynchronous programming concepts
- Familiarity with common data processing libraries (pandas, polars)

### Basic Implementation Example

The following example demonstrates how to set up a complete MSMTF system that aligns and processes data from multiple symbols across multiple timeframes:

```python
import datetime
import json
import os
import signal
from time import sleep
from typing import Dict, List

import pandas as pd
import polars as pl
from loguru import logger

from aitrados_api import SubscribeEndpoint, ChartDataFormat
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient
from aitrados_api import WebSocketClient
from aitrados_api import LatestOhlcMultiTimeframeManager
from aitrados_api import IntervalName

api_config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
    debug=True
)
api_client=DatasetClient(config=api_config)


def show_subscribe_handle_msg(client: WebSocketClient, message):
    print("subscriptions",json.dumps(client.all_subscribed_topics))


ws_client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
    is_reconnect=True,
    show_subscribe_handle_msg=show_subscribe_handle_msg,
    endpoint=SubscribeEndpoint.REALTIME,
    debug=True
)


def multi_timeframe_callback(name,data:Dict[str, List[str | list | pl.DataFrame | pd.DataFrame]],**kwargs):



    print(f"==================Received data:{name}========================{datetime.datetime.now()}")

    for full_symbol, tf_data_list in data.items():
        for tf_data in tf_data_list:
            if isinstance(tf_data, list):
                print(json.dumps(tf_data[-2:],indent=2),"===len===",len(tf_data))
            else:
                print(tf_data)




latest_ohlc_multi_timeframe_manager=LatestOhlcMultiTimeframeManager(
    api_client=api_client,
    ws_client=ws_client,
    multi_timeframe_callback=multi_timeframe_callback,
    limit=150,#data length limit
    works=10,
    data_format=ChartDataFormat.DICT #multi_timeframe_callback return data format
)





is_close=False
def signal_handler(sig, frame):
    ws_client.close()
    global is_close
    is_close=True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    ws_client.run(is_thread=True)

    # Add single symbol with single timeframe
    latest_ohlc_multi_timeframe_manager.add_item(
        item_data={
            "CRYPTO:GLOBAL:BTCUSD": [ IntervalName.M60],
        },
        name="single_timeframe"
    )

    # Add single symbol with multiple timeframes
    latest_ohlc_multi_timeframe_manager.add_item(
        item_data={
            "CRYPTO:GLOBAL:BTCUSD": [ IntervalName.M60, IntervalName.DAY],
        },
        name="multi_timeframe"
    )

    # Add multiple symbols with multiple timeframes
    latest_ohlc_multi_timeframe_manager.add_item(
        item_data={
            "CRYPTO:GLOBAL:BTCUSD": [IntervalName.M15, IntervalName.M60, IntervalName.DAY],
            "CRYPTO:GLOBAL:ETHUSD": [IntervalName.M15, IntervalName.M60, IntervalName.DAY]
        },
        name="multi_symbol_multi_timeframe"
    )

    # Add multiple stocks with multiple timeframes

    latest_ohlc_multi_timeframe_manager.add_item(
        item_data={
            "stock:us:tsla": [IntervalName.M5, IntervalName.M60, IntervalName.DAY],
            "stock:us:spy":[IntervalName.M5, IntervalName.M60, IntervalName.WEEK],
        },
        name="stock_multi_timeframe"
    )

    while not is_close:
        sleep(2)
    # Remove item example
    #latest_ohlc_multi_timeframe_manager.remove_item(name="multi_symbol_multi_timeframe")
    #latest_ohlc_multi_timeframe_manager.remove_item(name="multi_timeframe")
    #latest_ohlc_multi_timeframe_manager.remove_item(name="single_timeframe")
    #latest_ohlc_multi_timeframe_manager.remove_item(name="stock_multi_timeframe")
    logger.info("Exited")


```

