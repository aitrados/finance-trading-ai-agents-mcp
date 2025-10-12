---
weight: 30
date: "2025-09-10T00:00:00+01:00"
draft: false
author: "VON"
title: "Latest OHLC Chart Flow Example"
toc: true
description: "A practical guide to implementing real-time OHLC chart data flow in your trading applications using the AiTrados API"
publishdate: "2025-09-10T00:00:00+01:00"
tags: ["OHLC", "Real-time", "Streaming", "WebSocket", "Example", "Python","Multi-Symbol,Multi-Timeframe (MSMTF)","Multi-Symbol","Multi-Timeframe (MTF)"]
---

# Implementing the Latest OHLC Chart Flow

This guide demonstrates how to implement a real-time OHLC chart flow in your trading applications using the AiTrados API. By following this example, you'll be able to maintain an always up-to-date series of price candles for any supported instrument and timeframe.

## Basic Implementation

Below is a complete, working example of how to set up and manage a real-time OHLC chart flow for Bitcoin (BTCUSD) with 1-minute candles:

```python
import json
import os
import signal
from time import sleep

import pandas as pd
import polars as pl
from aitrados_api import SubscribeEndpoint, ChartDataFormat
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient
from aitrados_api import WebSocketClient
from aitrados_api import LatestOhlcChartFlowManager
from aitrados_api.common_lib.contant import IntervalName

api_config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    debug=True
)
api_client = DatasetClient(config=api_config)


def show_subscribe_handle_msg(client: WebSocketClient, message):
    print("subscriptions", json.dumps(client.all_subscribed_topics))


ws_client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    show_subscribe_handle_msg=show_subscribe_handle_msg,
    endpoint=SubscribeEndpoint.REALTIME,
    debug=True
)


def latest_ohlc_chart_flow_callback(data: str | list | dict | pd.DataFrame | pl.DataFrame):
    if isinstance(data, list):
        print("Received data:", json.dumps(data[-2:], indent=2))
    else:
        print("Received data:", data)


latest_ohlc_chart_flow_manager = LatestOhlcChartFlowManager(
    latest_ohlc_chart_flow_callback=latest_ohlc_chart_flow_callback,
    api_client=api_client,
    ws_client=ws_client,
    limit=150,
    data_format=ChartDataFormat.DICT
)

is_close = False


def signal_handler(sig, frame):
    ws_client.close()
    global is_close
    is_close = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    ws_client.run(is_thread=True)

    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M1)
    '''
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M3)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M5)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M10)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M15)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M60)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M120)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M240)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.WEEK)
    latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.MON)
    '''
    while not is_close:
        sleep(2)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M1)
    '''
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M3)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M5)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M10)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M15)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M60)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M120)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M240)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.WEEK)
    latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.MON)
    '''
```

## Understanding the Components

Let's break down the key components of the code example:

### 1. Setup and Configuration

```python
api_config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    debug=True
)
api_client = DatasetClient(config=api_config)

ws_client = WebSocketClient(
    secret_key=os.getenv("AITRADOS_SECRET_KEY", "YOUR_SECRET_KEY"),
    show_subscribe_handle_msg=show_subscribe_handle_msg,
    endpoint=SubscribeEndpoint.REALTIME,
    debug=True
)
```

This section initializes the core API clients:
- `DatasetClient`: Used for fetching historical data
- `WebSocketClient`: Handles the real-time data stream

### 2. Defining Your Data Handler

```python
def latest_ohlc_chart_flow_callback(data: str | list | dict | pd.DataFrame | pl.DataFrame):
    if isinstance(data, list):
        print("Received data:", json.dumps(data[-2:], indent=2))
    else:
        print("Received data:", data)
```

This callback function is called every time new data is available. It can receive data in various formats, depending on your configuration (JSON, DataFrame, etc.). In this simple example, we just print the last two candles for demonstration purposes. In a real application, you would:

- Process the data (calculate indicators, apply your strategy logic, etc.)
- Generate trading signals
- Execute trades
- Update your UI (if you have one)

### 3. Initializing the Manager

```python
latest_ohlc_chart_flow_manager = LatestOhlcChartFlowManager(
    latest_ohlc_chart_flow_callback=latest_ohlc_chart_flow_callback,
    api_client=api_client,
    ws_client=ws_client,
    limit=150,
    data_format=ChartDataFormat.DICT
)
```

The `LatestOhlcChartFlowManager` is the central component that handles:
- Initial data loading (the most recent 150 candles in this example)
- WebSocket subscription for real-time updates
- Data format conversion
- Callback invocation
- Automatic candle management (updating the latest candle, adding new ones, etc.)

Key parameters:
- `limit`: The number of candles to maintain
- `data_format`: The format in which data will be provided to your callback (DICT, POLARS, PANDAS)

### 4. Adding Chart Subscriptions

```python
latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M1)
```

This single line does all the heavy lifting:
1. Fetches the last 150 historical 1-minute candles for Bitcoin
2. Sets up a WebSocket subscription for real-time updates
3. Starts the continuous process of updating the chart data

### 5. Handling Multiple Timeframes

The commented-out section shows how easy it is to monitor multiple timeframes simultaneously:

```python
latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M3)
latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M5)
latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M10)
# ... and so on
```

This allows you to implement sophisticated multi-timeframe strategies with minimal code.

### 6. Cleanup and Resource Management

```python
latest_ohlc_chart_flow_manager.remove_item("crypto:global:btcusd", IntervalName.M1)
```

When you're done with a particular chart flow, you can remove it to conserve resources and network bandwidth.

## Advanced Use Cases

### Trading Strategy Implementation

Here's how you might modify the callback to implement a simple moving average crossover strategy:

```python
def trading_strategy_callback(data: list):
    # Extract just the complete candles (not the current forming one)
    complete_candles = data[:-1]  

    # Convert to pandas for easy analysis
    df = pd.DataFrame(complete_candles)

    # Calculate moving averages
    df['ma_fast'] = df['close'].rolling(window=20).mean()
    df['ma_slow'] = df['close'].rolling(window=50).mean()

    # Generate signals
    if df['ma_fast'].iloc[-1] > df['ma_slow'].iloc[-1] and df['ma_fast'].iloc[-2] <= df['ma_slow'].iloc[-2]:
        print(f"BUY SIGNAL: Fast MA crossed above Slow MA at {df['close'].iloc[-1]}")
        # Place buy order logic here

    elif df['ma_fast'].iloc[-1] < df['ma_slow'].iloc[-1] and df['ma_fast'].iloc[-2] >= df['ma_slow'].iloc[-2]:
        print(f"SELL SIGNAL: Fast MA crossed below Slow MA at {df['close'].iloc[-1]}")
        # Place sell order logic here
```

### Multi-Asset Portfolio Monitoring

You can easily expand the example to track multiple assets:

```python
# Bitcoin 1-minute chart
latest_ohlc_chart_flow_manager.add_item("crypto:global:btcusd", IntervalName.M1)

# Ethereum 1-minute chart
latest_ohlc_chart_flow_manager.add_item("crypto:global:ethusd", IntervalName.M1)

# S&P 500 ETF 5-minute chart
latest_ohlc_chart_flow_manager.add_item("stock:us:spy", IntervalName.M5)

# Gold futures 15-minute chart
latest_ohlc_chart_flow_manager.add_item("future:us:gc", IntervalName.M15)
```

### Automated Trading System

For a complete automated trading system, you would extend the callback to include order execution:

```python
def automated_trading_callback(data: list):
    # Strategy logic to generate signals
    signal = analyze_market_data(data)

    if signal == "BUY" and not position_open:
        # Execute buy order
        order_id = execute_buy_order("crypto:global:btcusd", quantity=0.1)
        position_open = True

    elif signal == "SELL" and position_open:
        # Execute sell order
        order_id = execute_sell_order("crypto:global:btcusd", quantity=0.1)
        position_open = False

    # Update dashboard/UI
    update_trading_dashboard(data, position_open, signal)
```

## Best Practices

For optimal implementation of the Latest OHLC Chart Flow, consider these best practices:

### 1. Error Handling

Always implement proper error handling in your callbacks:

```python
def robust_callback(data):
    try:
        # Process data and execute strategy
        process_data_and_trade(data)
    except Exception as e:
        logger.error(f"Error processing chart data: {e}")
        # Consider implementing retry logic or alerts
```

### 2. Resource Management

Be mindful of system resources, especially when subscribing to multiple instruments and timeframes:

- Subscribe only to the data you need
- Use appropriate `limit` values based on your strategy requirements
- Properly clean up resources when not needed

### 3. Handling Data Format Transitions

When you want more control over data processing:

```python
# For complex analysis, Pandas or Polars formats are often easier to work with
latest_ohlc_chart_flow_manager = LatestOhlcChartFlowManager(
    latest_ohlc_chart_flow_callback=latest_ohlc_chart_flow_callback,
    api_client=api_client,
    ws_client=ws_client,
    limit=150,
    data_format=ChartDataFormat.PANDAS  # or POLARS
)
```

### 4. Production Considerations

For production systems:

- Set `debug=False` to reduce console output
- Consider implementing logging to files instead of print statements
- Add monitoring for WebSocket connection health
- Implement reconnection logic for better resilience

## Conclusion

The `LatestOhlcChartFlowManager` provides a powerful yet simple way to maintain a real-time view of market data. By abstracting away the complexities of data synchronization and WebSocket management, it allows developers to focus on what really matters: implementing effective trading strategies.

Whether you're building a simple alerting tool or a sophisticated multi-asset trading system, the pattern demonstrated in this example provides a solid foundation for all your real-time market data needs.

For more information, see:
- [Intervals documentation](/docs/api/terminology/interval/) for supported timeframes
- [OHLC Data Reference](/docs/api/ohlc/latest_ohlc/) for details on the data structure
- [WebSocket API Guide](/docs/api/websocket/) for advanced WebSocket options