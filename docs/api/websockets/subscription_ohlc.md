---
weight: 20
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "OHLC Data Subscription"
toc: true
description: "Guide to subscribing to real-time OHLC market data via WebSockets"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "WebSocket", "OHLC", "Real-time", "Market Data"]
---

## Overview

This guide provides detailed instructions on how to subscribe to 1-minute candlestick (OHLC) market data using the AiTrados WebSocket API. Real-time OHLC data allows you to receive up-to-date price information for various assets, enabling timely market analysis and trading decisions.

## Subscription Endpoints

The AiTrados WebSocket API offers two endpoints for subscribing to OHLC data:

- [WebSocket Subscription Endpoint](/docs/api/websockets/subscription_endpoint/)

## Subscribing to OHLC Data

### Basic Subscription

To subscribe to 1-minute candlestick data, send the following message:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "ohlc",
    "topics": ["CRYPTO:GLOBAL:BTCUSD"]
  }
}
```

### Default Subscription

When you don't specify a `subscribe_type`, the system defaults to 1-minute candlestick data (`ohlc`):

```json
{
  "message_type": "subscribe",
  "params": {
    "topics": ["CRYPTO:GLOBAL:BTCUSD"]
  }
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message_type` | string | Yes | Must be set to "subscribe" for subscription requests |
| `params` | object | Yes | Contains subscription parameters |
| `params.subscribe_type` | string | No | Type of data to subscribe to (defaults to "ohlc") |
| `params.topics` | array | Yes | Array of assets to subscribe to using [full symbol format](/docs/api/terminology/full_symbol/) |

### Checking Current Subscriptions

To query all active subscriptions for the current connection:

```json
{
  "message_type": "show_subscribe"
}
```

### Unsubscribing

To unsubscribe from specific topics:

```json
{
  "message_type": "unsubscribe",
  "params": {
    "topics": ["CRYPTO:GLOBAL:BTCUSD"]
  }
}
```

## OHLC Data Structure

When subscribed, you will receive OHLC data with the following structure:

```json
{
  "message_type": "ohlc",
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": [
    {
      "asset_schema": "crypto",
      "country_iso_code": "GLOBAL",
      "exchange": "GLOBAL",
      "symbol": "BTCUSD",
      "datetime": "2025-09-14T10:55:00+00:00",
      "close_datetime": "2025-09-14T10:56:00+00:00",
      "open": 116080.58,
      "high": 116080.59,
      "low": 116036.8,
      "close": 116077.28,
      "volume": 0.15742726,
      "trading_session": "RTH",
      "interval": "1M",
      "vwap": 77372.51580908668
    }
  ]
}
```

## Python Implementation Example

The following example demonstrates how to subscribe to OHLC data using the AiTrados Python client library:

```python
import os
import signal
from aitrados_api.common_lib.common import logger
from aitrados_api import SubscribeEndpoint
from aitrados_api import WebSocketClient


def handle_msg(client: WebSocketClient, message):
    # Generic message handler
    pass


def ohlc_handle_msg(client: WebSocketClient, data_list):
    # Handler for OHLC data messages
    count = len(data_list)
    first_asset_schema = data_list[0].get('asset_schema', 'N/A')

    logger.info(
        f"Real-time data: Received 'ohlc_data' containing {count} records "
        f"(asset type: {first_asset_schema}) "
        f"{data_list[0].get('time_key_timestamp', 'N/A')}")


def show_subscribe_handle_msg(client: WebSocketClient, message):
    # Handler for subscription status messages
    logger.info(f"✅ Subscription status: {message}")
    print("subscriptions", client.all_subscribed_topics)


def auth_handle_msg(client: WebSocketClient, message):
    # Handler for authentication messages
    if not client.authorized:
        return

    # Subscribe to multiple assets after successful authentication
    client.subscribe_ohlc_1m("STOCK:US:SYMBOL", "CRYPTO:GLOBAL:SYMBOL", "FOREX:GLOBAL:SYMBOL")


# Initialize WebSocket client
client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    is_reconnect=True,
    handle_msg=handle_msg,
    ohlc_handle_msg=ohlc_handle_msg,
    show_subscribe_handle_msg=show_subscribe_handle_msg,
    auth_handle_msg=auth_handle_msg,
    endpoint=SubscribeEndpoint.DELAYED,  # Use DELAYED or REALTIME
    debug=False
)


def signal_handler(sig, frame):
    client.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    client.run(is_thread=False)
    # If running in a thread, you might need a loop:
    # while True:
    #     sleep(2)
```

## Client Configuration Options

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secret_key` | string | Yes | - | Your API secret key for authentication |
| `is_reconnect` | boolean | No | `True` | Whether to automatically reconnect on connection loss |
| `handle_msg` | function | No | - | Generic message handler function |
| `ohlc_handle_msg` | function | No | - | Handler for OHLC data messages |
| `show_subscribe_handle_msg` | function | No | - | Handler for subscription status messages |
| `auth_handle_msg` | function | No | - | Handler for authentication messages |
| `endpoint` | enum | No | `REALTIME` | Endpoint to connect to (`REALTIME` or `DELAYED`) |
| `debug` | boolean | No | `False` | Enable debug logging |

## Best Practices

1. **Connection Management**:
   - Implement proper reconnection logic using the `is_reconnect` parameter
   - Handle connection errors gracefully in production environments

2. **Subscription Efficiency**:
   - Only subscribe to assets you need to minimize network traffic
   - Group subscriptions where possible rather than making multiple individual requests

3. **Data Processing**:
   - Process incoming data efficiently, especially with high-frequency updates
   - Consider using buffering or batch processing for high-volume data

4. **Security**:
   - Never hardcode your secret key in your application
   - Use environment variables or secure key management solutions


## Related Documentation

- [WebSocket Testing Guide](/docs/api/websockets/websocket_testing_guide/)
- [Economic Events Subscription](/docs/api/websockets/subscription_economic_event/)
- [Full Symbol Format](/docs/api/terminology/full_symbol/)
