---
weight: 10
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Historical OHLC Data"
toc: true
description: "Retrieve historical price data for any supported asset"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["API", "OHLC", "Historical Data"]
---

## Historical OHLC Endpoint

Retrieve historical Open, High, Low, Close price data for any supported asset across various time intervals.

### Endpoint URL

```
GET /api/v2/{schema_asset}/bars/{country_symbol}/{interval}/from/{from_date}/to/{to_date}
```

### Description

This endpoint returns historical price data (candlesticks/bars) for the specified asset within the given time range. The data includes open, high, low, close prices, as well as volume and VWAP (Volume Weighted Average Price) when available.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description                                                                            |
|-----------|------|----------|----------------------------------------------------------------------------------------|
| `schema_asset` | string | Yes | Asset type, see [Asset Types](/docs/api/terminology/asset_name/)                       |
| `country_symbol` | string | Yes | Country and symbol format, see [Country Symbol](/docs/api/terminology/country_symbol/) |
| `interval` | string | Yes | Time interval Timeframe, see [Intervals](/docs/api/terminology/interval/)                       |
| `from_date` | datetime | Yes | Start date/time                                                                        |
| `to_date` | datetime | Yes | End date/time                                                                          |

### Query Parameters

| Parameter       | Type | Required | Default | Description                                             |
|-----------------|------|----------|---------|---------------------------------------------------------|
| `secret_key`    | string | Yes | -       | Your API secret key                                     |
| `format`        | string | No | "json"  | Response format ("json" or "csv")                       |
| `limit`         | integer | No | 150     | Maximum number of data points to return (max: 1000)     |
| `sort`          | string | No | 'asc'   | Sort direction ("asc" or "desc")                                            |
| `is_eth`     | boolean | No       | false   | Set to `true` to include data from extended trading hours for US stocks.    |
| `next_page_key` | string | No | -       | Pagination token for retrieving the next set of results |

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
| `result.next_page_key` | string | Token to retrieve the next page of results |
| `result.next_page_url` | string | Full URL to retrieve the next page |
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
GET https://default.dataset-api.aitrados.com/api/v2/crypto/bars/GLOBAL:BTCUSD/1M/from/2025-07-18T00:00:00+00:00/to/2025-09-05T23:59:59+00:00?format=json&limit=2&secret_key=your-secret-key
```

## Example Response

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "next_page_key": "b00631677a0d463ba8be810f73f5875a9f55c8a6f8a242d0c240e01bd9f56c01",
    "next_page_url": "http://default.dataset-api.aitrados.com/api/v2/crypto/bars/GLOBAL:BTCUSD/1M/from/2025-07-18T00:00:00+00:00/to/2025-09-05T23:59:59+00:00?format=json&limit=2&secret_key=your-secret-key&next_page_key=b00631677a0d463ba8be810f73f5875a9f55c8a6f8a242d0c240e01bd9f56c01",
    "count": 2,
    "data": [
      {
        "asset_schema": "CRYPTO",
        "interval": "1M",
        "country_iso_code": "GLOBAL",
        "exchange": "GLOBAL",
        "symbol": "BTCUSD",
        "datetime": "2025-07-18T00:30:00+00:00",
        "close_datetime": "2025-07-18T00:31:00+00:00",
        "open": 119584.44,
        "high": 119648.93,
        "low": 119499.2,
        "close": 119648.93,
        "volume": 3.0001965,
        "vwap": 79717.0433988
      },
      {
        "asset_schema": "CRYPTO",
        "interval": "1M",
        "country_iso_code": "GLOBAL",
        "exchange": "GLOBAL",
        "symbol": "BTCUSD",
        "datetime": "2025-07-18T00:31:00+00:00",
        "close_datetime": "2025-07-18T00:32:00+00:00",
        "open": 119648.93,
        "high": 119655.29,
        "low": 119504.8,
        "close": 119511.1,
        "volume": 3.7968731,
        "vwap": 79721.2956244
      }
    ]
  }
}
```

## Pagination 

When the result set exceeds the `limit` parameter, the response includes a `next_page_key` that can be used to retrieve the next set of results. To fetch the next page, include the `next_page_key` in your next request. Alternatively, you can directly use the `next_page_url` provided in the response.


## Code Examples

### Python

```python
import os
from aitrados_api import SchemaAsset
from aitrados_api import ClientConfig, RateLimitConfig
from aitrados_api import  DatasetClient


config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)

client=DatasetClient(config=config)
params = {
    "schema_asset": SchemaAsset.CRYPTO,
    "country_symbol": "GLOBAL:BTCUSD",
    "interval": "1m",
    "from_date": "2025-07-18T00:00:00Z",
    "to_date": "2025-09-05T23:59:59Z",
    "format": "json",
    "limit": 30
}
#***************************************OHLC DATA***************************#

## Get historical OHLC data
for ohlc in client.ohlc.ohlcs(**params):
    print(ohlc)
```