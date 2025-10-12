---
title: "Symbol Reference"
weight: 10
description: "Retrieve detailed information about financial instruments"
icon: "edit"
date: "2025-09-14T00:00:00+01:00"
lastmod: "2025-09-14T00:00:00+01:00"
draft: false
toc: true
tags: ["API", "Reference", "Asset Information"]
---

## Symbol Reference Endpoint

Retrieve detailed information about any supported financial instrument, including trading hours, exchange information, and asset properties.

### Endpoint URL

```
GET /api/v2/{schema_asset}/reference/{country_symbol}
```

### Description

This endpoint returns comprehensive reference data for the specified asset. The data varies by asset type, with stocks, forex, and cryptocurrencies each returning type-specific information.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schema_asset` | string | Yes | Asset type, see [Asset Types](/docs/api/terminology/asset_name/) |
| `country_symbol` | string | Yes | Country and symbol format, see [Country Symbol](/docs/api/terminology/country_symbol/) |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secret_key` | string | Yes | - | Your API secret key |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Status of the request ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference source ("cached" if data is from cache) |
| `result` | object | Result container with asset reference data |

### Common Reference Data Fields

The following fields are common across most asset types:

| Field | Type | Description |
|-------|------|-------------|
| `asset_schema` | string | Asset type (STOCK, CRYPTO, FOREX, etc.) |
| `symbol` | string | Trading symbol |
| `name` | string | Full name of the asset |
| `exchange` | string | Exchange where the asset is traded |
| `country_iso_code` | string | Country/market code |
| `currency` | string | Trading currency |
| `time_zone` | string | Time zone of the exchange |
| `open_time` | string | Market open time |
| `close_time` | string | Market close time |
| `trading_hours` | object | Detailed trading session hours |
| `status` | string | Current trading status |

### Asset-Specific Fields

Different asset types return additional fields relevant to that asset class:

#### Stock-Specific Fields

Stocks include additional fields such as:
- Pre/post market trading hours
- Exchange-specific identifiers
- Session templates

#### Forex-Specific Fields

Forex pairs include:
- `base_currency`: The base currency in the pair
- `quote_currency`: The quote currency in the pair

#### Crypto-Specific Fields

Cryptocurrencies include:
- `base_currency`: The cryptocurrency being traded
- `quote_currency`: The currency used for pricing

## Example Requests

### Stock Example

```
GET https://default.dataset-api.aitrados.com/api/v2/stock/reference/US:TSLA?secret_key=your-secret-key
```

### Forex Example

```
GET https://default.dataset-api.aitrados.com/api/v2/forex/reference/GLOBAL:EURUSD?secret_key=your-secret-key
```

### Cryptocurrency Example

```
GET https://default.dataset-api.aitrados.com/api/v2/crypto/reference/GLOBAL:BTCUSD?secret_key=your-secret-key
```

## Code Examples

### Python

```python
import os
from aitrados_api import SchemaAsset
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient

config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)

client = DatasetClient(config=config)

# Get stock reference data
stock_reference = client.reference.reference(schema_asset=SchemaAsset.STOCK, country_symbol="US:TSLA")

# Get cryptocurrency reference data
crypto_reference = client.reference.reference(schema_asset=SchemaAsset.CRYPTO, country_symbol="GLOBAL:BTCUSD")

# Get forex pair reference data
forex_reference = client.reference.reference(schema_asset=SchemaAsset.FOREX, country_symbol="GLOBAL:EURUSD")
```

## Example Responses
#### stock
```json

{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": "cached",
  "result": {
    "exchange": "XNAS",
    "name": "Tesla, Inc. Common Stock",
    "currency": "USD",
    "calendar_key": "US_STOCK",
    "open_time": "09:30:00",
    "description": null,
    "asset_subtype": null,
    "support_dst": false,
    "time_zone": "America/New_York",
    "underlying_name": "TSLA",
    "country_iso_code": "US",
    "session_template": "US_STOCK_RTH",
    "trading_hours": {
      "regular_trading": [
        "09:30:00-16:00:00"
      ],
      "pre_market_trading": [
        "04:00:00-09:30:00"
      ],
      "post_market_trading": [
        "16:00:00-20:00:00"
      ]
    },
    "close_time": "16:00:00",
    "asset_schema": "stock",
    "industry": null,
    "support_week_trading": true,
    "instrument_id": 100997,
    "asset_id": 998,
    "symbol": "TSLA",
    "trading_codes": null,
    "is_indices": false,
    "status": "active",
    "parent_schema_instrument_id": null,
    "daily_minute_count": 390,
    "contract_type": null,
    "contract_value": "1",
    "price_precision": null,
    "quantity_precision": null,
    "min_initial_open_quantity": null,
    "tick_size": null,
    "lot_size": null,
    "listing_date": null
  }
}
```
#### forex
```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": "cached",
  "result": {
    "exchange": "GLOBAL",
    "name": "Euro-USD",
    "currency": "USD",
    "calendar_key": "FOREX_GLOBAL",
    "open_time": "00:02:00",
    "description": null,
    "asset_subtype": null,
    "support_dst": false,
    "time_zone": "UTC",
    "underlying_name": "EURUSD",
    "country_iso_code": "GLOBAL",
    "session_template": "FOREX_GLOBAL",
    "trading_hours": {
      "regular_trading": [
        "00:02:00-23:58:00"
      ]
    },
    "close_time": "23:58:00",
    "asset_schema": "forex",
    "industry": null,
    "support_week_trading": false,
    "instrument_id": 300374,
    "asset_id": 2983,
    "symbol": "EURUSD",
    "trading_codes": null,
    "is_indices": false,
    "status": "active",
    "parent_schema_instrument_id": null,
    "daily_minute_count": 1436,
    "contract_type": null,
    "contract_value": "1",
    "price_precision": null,
    "quantity_precision": null,
    "min_initial_open_quantity": null,
    "tick_size": null,
    "lot_size": null,
    "listing_date": null,
    "base_currency": "EUR",
    "quote_currency": "USD"
  }
}
```
#### crypto
```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": "cached",
  "result": {
    "name": "Bitcoin-USD",
    "exchange": "GLOBAL",
    "currency": "USD",
    "calendar_key": "CRYPTO_GLOBAL",
    "open_time": "00:00:00",
    "description": null,
    "asset_subtype": null,
    "support_dst": false,
    "time_zone": "UTC",
    "country_iso_code": "GLOBAL",
    "underlying_name": "BTCUSD",
    "session_template": "CRYPTO_GLOBAL",
    "trading_hours": {
      "regular_trading": [
        "00:00:00-23:59:59"
      ]
    },
    "close_time": "23:59:00",
    "asset_schema": "crypto",
    "industry": null,
    "support_week_trading": true,
    "instrument_id": 500003,
    "asset_id": 2481,
    "symbol": "BTCUSD",
    "trading_codes": null,
    "is_indices": false,
    "status": "active",
    "parent_schema_instrument_id": null,
    "daily_minute_count": 1440,
    "contract_type": null,
    "contract_value": "1",
    "price_precision": null,
    "quantity_precision": null,
    "min_initial_open_quantity": null,
    "tick_size": null,
    "lot_size": null,
    "listing_date": null,
    "base_currency": "BTC",
    "quote_currency": "USD"
  }
}

```
## Usage Notes

1. Reference data is useful for determining:
   - Trading hours and market availability
   - Currency and quote information
   - Exchange details
   - Asset properties

2. Different asset classes return different sets of fields, so your application should be prepared to handle varying response structures based on the asset type.

3. Reference data is typically cached and updated periodically, so the `reference` field in the response may indicate `cached` for frequently accessed instruments.
