---
weight: 1
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Country Symbol"
toc: true
description: "Understanding the country_symbol parameter in AiTrados API"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["Beginners", "API", "Python"]

---

## Country Symbol Format

Due to AiTrados' distributed server architecture, some API endpoints use the `country_symbol` parameter instead of the full symbol notation. This is particularly common in the OHLC (Open, High, Low, Close) data retrieval endpoints.

The `country_symbol` parameter combines the country/market code and the specific symbol in the format:

```
COUNTRY:SYMBOL
```

This is essentially the last two components of the `full_symbol` format (`ASSET_TYPE:COUNTRY:SYMBOL`).

## Examples

Here are examples of `country_symbol` values for different asset types:

| Asset Type | country_symbol |
|------------|----------------|
| Stock      | `US:AAPL`      | 
| Forex      | `GLOBAL:EURUSD` | 
| Crypto     | `GLOBAL:BTCUSDT` |
| Future     | `US:ESU23`     |
| Option     | `US:SPY250707C00450000` | 

## When to Use country_symbol

The `country_symbol` parameter is typically used in these scenarios:

1. When the asset type is already specified through another parameter or context
2. When querying OHLC data where the server routes requests based on country/market
3. In subscription endpoints where you're already filtering by asset type

## API Usage Examples

### OHLC Data Retrieval

```python
# Example of using country_symbol in an OHLC API call
from aitrados_api import Client, SchemaAsset

client = Client(api_key="YOUR_API_KEY")

# Method 1: Using country_symbol with asset_type
ohlc_data = client.get_ohlc(
    asset_type=SchemaAsset.CRYPTO,
    country_symbol="GLOBAL:BTCUSDT",
)

# Method 2: Using full_symbol directly
ohlc_data = client.get_ohlc(
    full_symbol="CRYPTO:GLOBAL:BTCUSDT",
)
```

## Available Country/Market Codes

Here are the common country codes used in the AiTrados API:

| Country Code | Description |
|--------------|-------------|
| `US`         | United States markets |
| `JP`         | Japanese markets |
| `HK`         | Hong Kong markets |
| `CN`         | Chinese markets |
| `UK`         | United Kingdom markets |
| `DE`         | German markets |
| `GLOBAL`     | Global markets (used for Forex and Crypto) |
| more country |  more country|

## Wildcard Support

Like the `full_symbol` parameter, `country_symbol` also supports wildcards to refer to all symbols in a specific market:

```python
# Subscribe to all US stocks
client.subscribe(
    asset_type=SchemaAsset.STOCK,
    country_symbol="US:*"
)

# Subscribe to all global cryptocurrencies
client.subscribe(
    asset_type=SchemaAsset.CRYPTO,
    country_symbol="GLOBAL:*"
)
```

