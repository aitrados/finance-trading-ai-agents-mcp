---
weight: 10
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "WebSocket Testing Guide"
toc: true
description: "A comprehensive guide to testing AiTrados WebSocket API using wscat"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "WebSocket", "Real-time", "Testing"]
---

## Introduction

This guide demonstrates how to quickly test the AiTrados WebSocket subscription service using `wscat`, a simple command-line tool. WebSockets provide real-time data streaming capabilities, allowing you to receive market data, news, and economic events as they happen.

## Prerequisites

Before you begin, ensure you have Node.js installed on your system. Then install the `wscat` tool globally using npm:

```bash
npm install -g wscat
```

## Connecting to the WebSocket Server

Use the following command to establish a connection to the AiTrados WebSocket server:

```bash
wscat -c wss://realtime.dataset-sub.aitrados.com/ws
```
Use delayed 15 minutes data server
```bash

wscat -c wss://delayed.dataset-sub.aitrados.com/ws
```

## Authentication

Once connected, you must authenticate using your secret key:

```json
{"message_type":"authenticate","params":{"secret_key":"your-secret-key"}}
```

**Response:**

```json
{"message_type":"authenticate","status":"ok","code":200,"message":"success","reference":null,"result":{"authenticated":true}}
```

## Subscribing to OHLC Data (1-Minute Candles)

### Single Asset Subscription

To subscribe to a single asset:

```json
{"message_type":"subscribe","params":{"topics":["CRYPTO:GLOBAL:BTCUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":["CRYPTO:GLOBAL:BTCUSD"]}}
```

### Checking Current Subscriptions

To view your current subscriptions:

```json
{"message_type":"show_subscribe"}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":["CRYPTO:GLOBAL:BTCUSD"]}}
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"event":[]}}
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"news":[]}}
```

### Unsubscribing from a Single Asset

To unsubscribe from a specific asset:

```json
{"message_type":"unsubscribe","params":{"topics":["CRYPTO:GLOBAL:BTCUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":[]}}
```

### Multiple Asset Subscription

To subscribe to multiple assets at once:

```json
{"message_type":"subscribe","params":{"topics":["STOCK:US:AAPL","CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":["CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD","STOCK:US:AAPL"]}}
```

### Unsubscribing from Multiple Assets

To unsubscribe from multiple assets at once:

```json
{"message_type":"unsubscribe","params":{"topics":["STOCK:US:AAPL","CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":[]}}
```

### Wildcard Subscription

To subscribe to all assets within specific categories using wildcards:

```json
{"message_type":"subscribe","params":{"topics":["STOCK:US:*","CRYPTO:GLOBAL:*","FOREX:GLOBAL:*"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":["CRYPTO:GLOBAL:*","FOREX:GLOBAL:*","STOCK:US:*"]}}
```

### Unsubscribing from Wildcard Subscriptions

To unsubscribe from wildcard subscriptions:

```json
{"message_type":"unsubscribe","params":{"topics":["STOCK:US:*","CRYPTO:GLOBAL:*","FOREX:GLOBAL:*"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"ohlc:1m":[]}}
```

## Subscribing to News Data

To subscribe to news related to specific assets:

```json
{"message_type":"subscribe","params":{"subscribe_type": "news","topics":["STOCK:US:AAPL","CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"news":["CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD","STOCK:US:AAPL"]}}
```

### Unsubscribing from News Data

To unsubscribe from news data:

```json
{"message_type":"unsubscribe","params":{"subscribe_type": "news","topics":["STOCK:US:AAPL","CRYPTO:GLOBAL:BTCUSD","FOREX:GLOBAL:EURUSD"]}}
```

**Response:**

```json
{"message_type":"show_subscribe","status":"ok","code":200,"message":"success","reference":null,"result":{"news":[]}}
```

## Subscribing to Economic Events

### Real-Time Economic Data

To subscribe to economic indicators (CPI and unemployment rate) and receive updates when data is published:

```json
{"message_type":"subscribe","params":{"subscribe_type": "event","topics":["US:INFLATION_CPI_NSA:REAL_TIME","US:UNEMPLOYMENT_RATE:REAL_TIME"]}}
```

```json
{"message_type":"subscribe","params":{"subscribe_type": "event","topics":["US:*:REAL_TIME"]}}
```
### Pre-Release Notifications

To receive notifications before economic data is released (available time periods: 30DAY, 2WEEK, 1WEEK, 1DAY, 60M, 15M, 5M):

```json
{"message_type":"subscribe","params":{"subscribe_type": "event","topics":["US:INFLATION_CPI_NSA:15M","US:UNEMPLOYMENT_RATE:15M"]}}
```

## Best Practices

1. **Efficient Subscriptions**: Only subscribe to the data you need to minimize bandwidth usage and improve performance.

2. **Error Handling**: Always implement proper error handling in your production applications to manage connection issues and unexpected responses.

3. **Reconnection Logic**: For production applications, implement automatic reconnection logic with exponential backoff.

4. **Authentication Security**: Never hardcode your secret key in client-side applications. Always use secure methods to store and retrieve your credentials.

5. **Data Processing**: When receiving high-frequency data, implement efficient data processing to avoid bottlenecks.

## Conclusion

This guide demonstrates the basic usage of the AiTrados WebSocket API using the `wscat` tool. For production applications, we recommend using appropriate WebSocket libraries for your programming language of choice, with proper error handling and reconnection logic.

For more detailed information about the response data formats and available topics, please refer to the [WebSocket API Reference](/docs/api/websockets/reference/).
