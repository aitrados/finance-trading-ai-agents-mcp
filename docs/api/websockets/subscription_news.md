---
weight: 25
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "News Data Subscription"
toc: true
description: "Guide to subscribing to real-time financial news data via WebSockets"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "WebSocket", "News", "Real-time", "Market Data"]
---

## Overview

This guide provides detailed instructions on how to subscribe to real-time news data for specific financial instruments using the AiTrados WebSocket API. Real-time news subscriptions allow you to receive the latest news, press releases, and announcements related to assets in your portfolio, enabling timely market analysis and informed trading decisions.

## News Subscription Benefits

- **Immediate Notifications**: Receive news as it happens
- **Filtered Content**: Subscribe only to news about specific assets of interest
- **Market Context**: Understand price movements in relation to news events
- **Trading Opportunities**: Identify potential trading opportunities based on breaking news
- **Risk Management**: Quickly react to events that might impact your positions

## Subscribing to News Data

### Basic Subscription

To subscribe to news data for specific assets, send the following message:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "news",
    "topics": ["STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD", "FOREX:GLOBAL:EURUSD"]
  }
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message_type` | string | Yes | Must be set to "subscribe" for subscription requests |
| `params` | object | Yes | Contains subscription parameters |
| `params.subscribe_type` | string | Yes | Must be set to "news" for news subscriptions |
| `params.topics` | array | Yes | Array of assets to subscribe to using [full symbol format](/docs/api/terminology/full_symbol/) |

### Checking Current Subscriptions

To query all active subscriptions for the current connection:

```json
{
  "message_type": "show_subscribe"
}
```

The response will include all your active subscriptions, including news subscriptions:

```json
{
  "message_type": "show_subscribe",
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "news": ["STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD", "FOREX:GLOBAL:EURUSD"]
  }
}
```

### Unsubscribing from News

To unsubscribe from news for specific assets:

```json
{
  "message_type": "unsubscribe",
  "params": {
    "subscribe_type": "news",
    "topics": ["STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD", "FOREX:GLOBAL:EURUSD"]
  }
}
```

## News Data Structure

When subscribed to news, you will receive data with the following structure:

```json
{
  "message_type": "news",
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": [
      {
        "sentiment_label": null,
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-07-01T02:57:14+00:00",
        "publisher": "reuters.com",
        "title": "Tesla registrations in Denmark fall 61.6% year-on-year in June",
        "text_content": "Tesla's registration of new cars in Denmark fell by 61.57% in June from the same month a year ago to 1,282 vehicles, registration data from Mobility Denmark showed on Tuesday.",
        "publisher_url": "https://www.reuters.com/business/autos-transportation/tesla-registrations-denmark-fall-616-year-on-year-june-2025-07-01/",
        "sentiment_score": null
      },
      {
        "sentiment_label": null,
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-07-01T03:49:51+00:00",
        "publisher": "reuters.com",
        "title": "Tesla sales drop over 60% in Sweden and Denmark",
        "text_content": "Tesla's sales dropped for a sixth straight month in Sweden and Denmark in June, underscoring the challenges the EV-maker faces as competitors gain market share and CEO Elon Musk's popularity declines.",
        "publisher_url": "https://www.reuters.com/business/autos-transportation/tesla-sales-drop-over-60-sweden-denmark-2025-07-01/",
        "sentiment_score": null
      }
    ]
}
```

### News Data Fields


## Python Implementation Example

The following example demonstrates how to subscribe to news data using the AiTrados Python client library:

```python
import os
import signal
from aitrados_api.common_lib.common import logger
from aitrados_api import SubscribeEndpoint
from aitrados_api import WebSocketClient


def handle_msg(client: WebSocketClient, message):
    # Generic message handler
    pass


def news_handle_msg(client: WebSocketClient, data_list):
    # Handler for news data messages
    for record in data_list:
        symbol = f"{record.get('asset_schema')}:{record.get('country_iso_code')}:{record.get('underlying_name')}"
        string = f"news:{symbol} --> {record.get('published_date')} --> {record.get('title')}"
        logger.info(string)


def show_subscribe_handle_msg(client: WebSocketClient, message):
    # Handler for subscription status messages
    logger.info(f"✅ Subscription status: {message}")
    print("subscriptions", client.all_subscribed_topics)


def auth_handle_msg(client: WebSocketClient, message):
    # Handler for authentication messages
    if not client.authorized:
        return

    # Subscribe to multiple assets after successful authentication
    client.subscribe_news("STOCK:US:AAPL", "CRYPTO:GLOBAL:BTCUSD", "FOREX:GLOBAL:EURUSD")


# Initialize WebSocket client
client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    is_reconnect=True,
    handle_msg=handle_msg,
    news_handle_msg=news_handle_msg,  # Specific handler for news data
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
| `news_handle_msg` | function | No | - | Handler specifically for news data messages |
| `show_subscribe_handle_msg` | function | No | - | Handler for subscription status messages |
| `auth_handle_msg` | function | No | - | Handler for authentication messages |
| `endpoint` | enum | No | `REALTIME` | Endpoint to connect to (`REALTIME` or `DELAYED`) |
| `debug` | boolean | No | `False` | Enable debug logging |

## News Filtering Strategies

### Asset Type Filtering

Subscribe to news for all assets of a specific type using wildcards:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "news",
    "topics": ["STOCK:US:*"]
  }
}
```


### Multi-Asset Portfolio Monitoring

For monitoring a diverse portfolio, subscribe to multiple specific assets:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "news",
    "topics": [
      "STOCK:US:AAPL", 
      "STOCK:US:MSFT", 
      "CRYPTO:GLOBAL:BTCUSD", 
      "FOREX:GLOBAL:EURUSD"
    ]
  }
}
```

## Best Practices

1. **Targeted Subscriptions**: Subscribe only to news for assets you're actively monitoring to reduce noise and improve relevance.

2. **Connection Management**: Implement proper reconnection logic with exponential backoff to handle temporary connection issues.

3. **News Processing**:
   - Filter news based on relevance score to focus on significant events
   - Consider sentiment analysis for automated trading signals
   - Store news data for historical analysis and pattern recognition

4. **Integration with Price Data**: Correlate news events with price movements for comprehensive market analysis.

5. **User Notifications**: When implementing a client application, set up alerts for high-impact news items.

## Rate Limits and Quotas

News subscription services are subject to rate limits based on your account tier. Please refer to the [Rate Limits](/docs/api/rate_limits/) documentation for details on your specific quota.

## Related Documentation

- [WebSocket Subscription Endpoints](/docs/api/websockets/subscription_endpoint/)
- [OHLC Data Subscription](/docs/api/websockets/subscription_ohlc/)
- [Economic Events Subscription](/docs/api/websockets/subscription_economic_event/)
- [Full Symbol Format](/docs/api/terminology/full_symbol/)

