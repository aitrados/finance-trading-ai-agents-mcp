---
weight: 20
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Latest OHLC Data"
toc: true
description: "Retrieve the most recent price data for supported assets"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["API", "OHLC", "Real-time Data"]
---

## Latest OHLC Endpoint

Retrieve the most recent Open, High, Low, Close price data for any supported asset.

### Endpoint URL

```
GET /api/v2/{schema_asset}/bars/{country_symbol}/{interval}/latest
```

### Description

This endpoint returns the most recent price data (candlesticks/bars) for the specified asset and interval. It's useful for getting the current state of the market without specifying a date range.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description                                                                            |
|-----------|------|----------|----------------------------------------------------------------------------------------|
| `schema_asset` | string | Yes | Asset type, see [Asset Types](/docs/api/terminology/asset_name/)                       |
| `country_symbol` | string | Yes | Country and symbol format, see [Country Symbol](/docs/api/terminology/country_symbol/) |
| `interval` | string | Yes | Time interval Timeframe, see [Intervals](/docs/api/terminology/interval/)               |

### Query Parameters

| Parameter | Type | Required | Default | Description                                             |
|-----------|------|----------|---------|---------------------------------------------------------|
| `secret_key` | string | Yes | -       | Your API secret key                                     |
| `format` | string | No | "json"  | Response format ("json" or "csv")                       |
| `limit` | integer | No | 150     | Number of most recent data points to return (max: 1000) |
| `is_eth`     | boolean | No       | false   | Set to `true` to include data from extended trading hours for US stocks.    |

### Supported Intervals

See [Intervals documentation](/docs/api/terminology/interval/) for detailed information.

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Status of the request ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | object | Result container |
| `result.count` | integer | Number of records in the current response |
| `result.data` | array | Array of OHLC data points |

### Data Point Fields

| Field | Type | Description |
|-------|------|-------------|
| `asset_schema` | string | Asset type (STOCK, CRYPTO, FOREX, etc.) |
| `interval` | string | Time interval of the data point |
| `country_iso_code` | string | Country code |
| `exchange` | string | Exchange where the asset is traded |
| `symbol` | string | Symbol of the asset |
| `datetime` | string | Open time of the candle (ISO 8601 format) |
| `close_datetime` | string | Close time of the candle (ISO 8601 format) |
| `open` | number | Opening price |
| `high` | number | Highest price during the interval |
| `low` | number | Lowest price during the interval |
| `close` | number | Closing price |
| `volume` | number | Trading volume |
| `vwap` | number | Volume Weighted Average Price (if available) |

## Example Request

```
GET https://default.dataset-api.aitrados.com/api/v2/crypto/bars/GLOBAL:BTCUSD/1M/latest?format=json&limit=2&secret_key=your-secret-key
```

## Example Response

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "count": 2,
    "data": [
      {
        "asset_schema": "CRYPTO",
        "interval": "1M",
        "country_iso_code": "GLOBAL",
        "exchange": "GLOBAL",
        "symbol": "BTCUSD",
        "datetime": "2025-09-13T16:03:00+00:00",
        "close_datetime": "2025-09-13T16:04:00+00:00",
        "open": 115858.47,
        "high": 115871.19,
        "low": 115786.5,
        "close": 115871.19,
        "volume": 2.6138306,
        "vwap": 77220.1012769
      },
      {
        "asset_schema": "CRYPTO",
        "interval": "1M",
        "country_iso_code": "GLOBAL",
        "exchange": "GLOBAL",
        "symbol": "BTCUSD",
        "datetime": "2025-09-13T16:04:00+00:00",
        "close_datetime": "2025-09-13T16:05:00+00:00",
        "open": 115870.01,
        "high": 115885,
        "low": 115750,
        "close": 115870.01,
        "volume": 8.4749461,
        "vwap": 77214.4916487
      }
    ]
  }
}
```

## Code Examples

### Python

```python
import os
from aitrados_api import SchemaAsset
from aitrados_api import ClientConfig, RateLimitConfig
from aitrados_api import DatasetClient


config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)

client=DatasetClient(config=config)
params = {
    "schema_asset": SchemaAsset.CRYPTO,
    "country_symbol": "GLOBAL:BTCUSD",
    "interval": "1m",
    "format": "json",
    "limit": 1
}

# Get latest OHLC data (for real-time data)
ohlc_latest = client.ohlc.ohlcs_latest(**params)
print(ohlc_latest)
```

## Market Hours Note

For assets that trade on exchanges with specific market hours (like stocks), the latest data will correspond to the most recent completed interval during market hours. For assets that trade 24/7 (like cryptocurrencies), the latest data will generally be up-to-date within the constraints of the chosen interval.
