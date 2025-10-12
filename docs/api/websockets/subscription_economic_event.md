---
weight: 30
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Economic Events Subscription"
toc: true
description: "Guide to subscribing to economic indicators and events via WebSockets"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "WebSocket", "Economic Events", "Indicators", "Real-time"]
---

## Overview

This guide provides detailed instructions on how to subscribe to economic events and indicators using the AiTrados WebSocket API. Economic events subscriptions allow you to receive real-time updates on key economic indicators such as inflation rates, unemployment figures, GDP data, and central bank decisions that can significantly impact financial markets.

## Why Subscribe to Economic Events

- **Market-Moving Data**: Economic indicators often cause significant market movements
- **Trading Opportunities**: Identify potential trading opportunities based on economic releases
- **Risk Management**: Prepare for market volatility around key economic announcements
- **Advance Notifications**: Receive alerts before important economic data releases
- **Cross-Market Analysis**: Understand how economic data affects various asset classes

## Economic Event Subscription

### Basic Subscription

To subscribe to specific economic events, send the following message:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "event",
    "topics": [
      "US:INFLATION_CPI_NSA:REAL_TIME",
      "US:UNEMPLOYMENT_RATE:REAL_TIME"
    ]
  }
}
```

### Wildcard Subscription

To subscribe to all economic events for specific countries:

```json
{
  "message_type": "subscribe",
  "params": {
    "subscribe_type": "event",
    "topics": ["US:*", "UK:*"]
  }
}
```

## Topic Format Specification

Each topic in the economic events subscription follows this format:

```
COUNTRY:EVENT_CODE:PREVIEW_INTERVAL
```

### Parameters Explanation

| Parameter | Description | Examples                                                           |
|-----------|-------------|--------------------------------------------------------------------|
| `COUNTRY` | ISO country code where the economic event occurs | `US`, `UK`, `EU`, `JP`, `CN`,`GLOBAL`                              |
| `EVENT_CODE` | Unique identifier for the economic indicator | [Economic Event Codes](/docs/api/economic_event/event_codes/)                |
| `PREVIEW_INTERVAL` | When to receive the notification relative to the event | `REAL_TIME`, `30DAY`, `2WEEK`, `1WEEK`, `1DAY`, `60M`, `15M`, `5M` |

### Available Event Codes

A comprehensive list of economic event codes is available in the [Economic Event Codes](/docs/api/economic_event/event_codes/) documentation. Some of the most frequently used event codes include:

| Event Code | Description | Typical Impact |
|------------|-------------|----------------|
| `INFLATION_CPI_NSA` | Consumer Price Index (Non-Seasonally Adjusted) | High |
| `UNEMPLOYMENT_RATE` | Unemployment Rate | High |
| `GDP_QOQ` | Gross Domestic Product (Quarter over Quarter) | High |
| `INTEREST_RATE` | Central Bank Interest Rate Decision | Very High |
| `RETAIL_SALES_MOM` | Retail Sales (Month over Month) | Medium |
| `PMI_MANUFACTURING` | Purchasing Managers' Index - Manufacturing | Medium |
| `NONFARM_PAYROLLS` | Non-Farm Payrolls (US) | Very High |

### Preview Intervals

The `PREVIEW_INTERVAL` parameter allows you to receive notifications at different times relative to the economic event:

| Interval | Description |
|----------|-------------|
| `REAL_TIME` | Receive data immediately when published (default) |
| `30DAY` | Receive notification 30 days before the event |
| `2WEEK` | Receive notification 2 weeks before the event |
| `1WEEK` | Receive notification 1 week before the event |
| `1DAY` | Receive notification 1 day before the event |
| `60M` | Receive notification 60 minutes before the event |
| `15M` | Receive notification 15 minutes before the event |
| `5M` | Receive notification 5 minutes before the event |

## Managing Subscriptions

### Checking Current Subscriptions

To query all active subscriptions for the current connection:

```json
{
  "message_type": "show_subscribe"
}
```

The response will include all your active subscriptions, including economic event subscriptions:

```json
{
  "message_type": "show_subscribe",
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "event": [
      "US:INFLATION_CPI_NSA:REAL_TIME",
      "US:UNEMPLOYMENT_RATE:REAL_TIME"
    ]
  }
}
```

### Unsubscribing from Events

To unsubscribe from specific economic events:

```json
{
  "message_type": "unsubscribe",
  "params": {
    "subscribe_type": "event",
    "topics": [
      "US:INFLATION_CPI_NSA:REAL_TIME",
      "US:UNEMPLOYMENT_RATE:REAL_TIME"
    ]
  }
}
```

## Economic Event Data Structure

When an economic event occurs or is scheduled, you will receive data with the following structure:

```json
{
  "message_type": "event",
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": [
      {
        "country_iso_code": "US",
        "event_code": "BUSINESS_PMI_NON_MANUFACTURING_ISM",
        "event_name": "ISM Non-Manufacturing PMI",
        "event_driven_type": "time_driven",
        "importance": 3,
        "impact": "high",
        "event_timestamp": "2024-08-05T13:00:00Z",
        "actual_value": 51.4,
        "previous_value": 48.8,
        "forecast_value": 51.4,
        "change": 2.6,
        "change_percent": 0.0,
        "period": "Jul",
        "unit": "N/A",
        "source_id": "460b29c68f3590c1a6500b719cf9b4fc41f16b09d3ebb2a6c337fe41c1a75040",
        "preview_interval": "REAL_TIME"
      }
    
    ]
}
```


## Python Implementation Example

The following example demonstrates how to subscribe to economic events using the AiTrados Python client library:

```python
import os
import signal
from aitrados_api.common_lib.common import logger
from aitrados_api import SubscribeEndpoint
from aitrados_api import WebSocketClient


def handle_msg(client: WebSocketClient, message):
    # Generic message handler
    pass


def event_handle_msg(client: WebSocketClient, data_list):
    # Handler for economic event messages
    for record in data_list:
        symbol = f"{record.get('country_iso_code')}:{record.get('event_code')}:{record.get('preview_interval')}"
        string = f"event:{symbol} --> {record.get('event_timestamp')}"
        logger.info(string)


def show_subscribe_handle_msg(client: WebSocketClient, message):
    # Handler for subscription status messages
    logger.info(f"✅ Subscription status: {message}")
    print("subscriptions", client.all_subscribed_topics)


def auth_handle_msg(client: WebSocketClient, message):
    # Handler for authentication messages
    if not client.authorized:
        return

    # Subscribe to economic events after successful authentication
    client.subscribe_event("US:INFLATION_CPI_NSA:REAL_TIME", "US:UNEMPLOYMENT_RATE:REAL_TIME")


# Initialize WebSocket client
client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    is_reconnect=True,
    handle_msg=handle_msg,
    event_handle_msg=event_handle_msg,  # Specific handler for economic events
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

## Subscription Strategies

### High-Impact Events Only

To focus on market-moving events and reduce noise:

```python
# Subscribe only to high-impact economic indicators
client.subscribe_event(
    "US:NONFARM_PAYROLLS:REAL_TIME",
    "US:INFLATION_CPI_NSA:REAL_TIME",
    "US:INTEREST_RATE:REAL_TIME",
    "US:GDP_QOQ:REAL_TIME"
)
```

### Multi-Region Monitoring

To monitor key indicators across multiple regions:

```python
# Monitor inflation across major economies
client.subscribe_event(
    "US:INFLATION_CPI_NSA:REAL_TIME",
    "EU:INFLATION_CPI_YOY:REAL_TIME",
    "UK:INFLATION_CPI_YOY:REAL_TIME",
    "JP:INFLATION_CPI_YOY:REAL_TIME"
)
```

### Advance Notifications

To receive advance notifications before important releases:

```python
# Get notifications at different intervals before NFP release
client.subscribe_event(
    "US:NONFARM_PAYROLLS:1DAY",  # 1 day before
    "US:NONFARM_PAYROLLS:60M",   # 60 minutes before
    "US:NONFARM_PAYROLLS:15M",   # 15 minutes before
    "US:NONFARM_PAYROLLS:REAL_TIME"  # Actual release
)
```

## Best Practices

1. **Strategic Subscriptions**: Focus on economic events relevant to your trading strategy and asset classes.

2. **Advance Planning**: Use preview intervals to prepare for market volatility around major economic releases.

3. **Complete Coverage**: For critical indicators, consider subscribing to both advance notifications and real-time data.

4. **Data Integration**: Correlate economic data with price movements for comprehensive market analysis.

5. **Automated Responses**: Develop predefined responses to different economic scenarios based on deviation from forecasts.

6. **Economic Calendar**: Use economic event subscriptions to build a real-time economic calendar for your organization.


## Related Documentation

- [Economic Event Codes](/docs/api/economic_event/event_codes/)
- [WebSocket Subscription Endpoints](/docs/api/websockets/subscription_endpoint/)
- [OHLC Data Subscription](/docs/api/websockets/subscription_ohlc/)
