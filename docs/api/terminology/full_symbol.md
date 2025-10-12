---
weight: 1
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Full Symbol"
toc: true
description: "Understanding the AiTrados full symbol notation"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["Beginners", "API", "Python"]

---

## Full Symbol Format

The AiTrados API is designed to accommodate different markets and instrument types from around the world. We use a standardized `full_symbol` format to uniquely identify each trading instrument, following this pattern:

```
ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL
```

Where:
- **ASSET_NAME**: The category of the financial instrument (STOCK, FOREX, CRYPTO,FUTURE,OPTION etc.)
- **COUNTRY**: The country iso code (US, JP,CN,UK,HK,AU, GLOBAL, etc.)
{{< alert context="info" >}}
If no region is specified, use `GLOBAL`
{{< /alert >}}
- **SYMBOL**: The specific ticker or identifier for the instrument

## Examples

Here are examples to help you understand how the `full_symbol` notation works across different asset classes:

### Stocks

| Full Symbol | Description |
|-------------|-------------|
| `STOCK:JP:N225` | Japan's Nikkei 225 Index |
| `STOCK:US:AAPL` | Apple Inc. (US Stock) |
| `STOCK:US:*` | All US stocks (wildcard) |

### Options

| Full Symbol | Description |
|-------------|-------------|
| `OPTION:US:SPY250707C00450000` | SPY call option, July 7, 2025, $450 strike |

### Forex

| Full Symbol | Description |
|-------------|-------------|
| `FOREX:GLOBAL:EURUSD` | Euro/US Dollar pair |
| `FOREX:GLOBAL:*` | All global forex pairs (wildcard) |

### Cryptocurrencies

| Full Symbol | Description |
|-------------|-------------|
| `CRYPTO:GLOBAL:BTCUSDT` | Bitcoin/USDT pair |
| `CRYPTO:GLOBAL:*` | All global cryptocurrencies (wildcard) |

### Futures

| Full Symbol | Description |
|-------------|-------------|
| `FUTURE:US:ESU23` | S&P 500 E-mini futures (September 2023) |
| `FUTURE:US:*` | All US futures (wildcard) |

## Using Wildcards

The `*` character can be used as a wildcard to represent all symbols within a particular asset class and country. This is particularly useful for subscription operations when you want to monitor all instruments of a certain type.

## API Usage

When making API calls, the `full_symbol` parameter is used to specify the exact instrument you want to query or subscribe to:

```python
# Example of using full_symbol in an API call
params = {
    "full_symbol": "CRYPTO:GLOBAL:BTCUSDT",
    # other parameters
}
```
