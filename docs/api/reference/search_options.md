---
weight: 20
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Options Search"
toc: true
description: "Search for option contracts based on various criteria"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Options"]
---

## Options Search Endpoint

Retrieve a list of option contracts based on underlying asset, expiration date, strike price, and moneyness.

### Endpoint URL

```
GET /api/v2/option/search/{schema_asset}/{country_symbol}/{option_type}/moneyness/{moneyness}
```

### Description

This endpoint allows users to search for option contracts based on various criteria such as option type (call/put), moneyness (in-the-money/out-of-the-money), strike price, and expiration date. Search results are grouped by expiration date.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schema_asset` | string | Yes | Asset type, see [Asset Types](/docs/api/terminology/asset_name/) |
| `country_symbol` | string | Yes | Country and symbol format, see [Country Symbol](/docs/api/terminology/country_symbol/) |
| `option_type` | string | Yes | Type of option ("call" or "put") |
| `moneyness` | string | Yes | Moneyness of the option ("in_the_money" or "out_of_the_money") |

### Query Parameters

| Parameter | Type | Required | Default | Description                                             |
|-----------|------|----------|---------|---------------------------------------------------------|
| `secret_key` | string | Yes | - | Your API secret key                                     |
| `ref_asset_price` | float | No | - | Reference asset price for moneyness calculation         |
| `strike_price` | float | No | - | Specific strike price to filter options                 |
| `expiration_date` | datetime | No | - | Expiration date of the options                          |
| `limit` | integer | No | 100 | Number of results to return                             |
| `sort_by` | string | No | - | Sorting criteria for the results.`sort_by=strike_price%20desc,expiration_date`                       |
| `next_page_key` | string | No | - | Pagination token for retrieving the next set of results |

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
| `result.next_page_key` | string | Token to retrieve the next page of results |
| `result.next_page_url` | string | Full URL to retrieve the next page |
| `result.expiration_datetimes` | array | List of expiration dates included in the response |
| `result.data` | object | Option data grouped by expiration date |

### Option Fields

| Field | Type | Description |
|-------|------|-------------|
| `instrument_id` | integer | Option contract ID |
| `asset_id` | integer | Asset ID |
| `symbol` | string | Option contract symbol |
| `country_iso_code` | string | Country code |
| `exchange` | string | Exchange |
| `underlying_name` | string | Underlying asset name |
| `calendar_key` | string | Calendar key |
| `session_template` | string | Trading session template |
| `status` | string | Option status |
| `parent_schema_instrument_id` | string | Parent asset ID |
| `daily_minute_count` | integer | Daily trading minutes |
| `contract_value` | number | Contract value |
| `option_exchange` | string | Option exchange |
| `parent_asset_schema` | string | Parent asset schema |
| `strike_price` | number | Strike price |
| `expiration_date` | string | Expiration date (date format) |
| `expiration_datetime` | string | Expiration datetime (ISO 8601 format) |
| `option_type` | string | Option type ("call" or "put") |
| `exercise_style` | string | Exercise style ("american" or "european") |

## Example Request

```
GET https://default.dataset-api.aitrados.com/api/v2/option/search/stock/US:spy/call/moneyness/in_the_money?ref_asset_price=450.5&limit=2&secret_key=your-secret-key
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
    "next_page_key": "865eefd860dba1445d98c0368891bab8d3bd942aa3e988233cd470d6dbddc3f117df9c0108f411f25f06790745e356ba7417bf9eeb82ec14c808abcd16daf3fbabc615c3444f9e604f5816d99e71166d",
    "next_page_url": "https://default.dataset-api.aitrados.com/api/v2/option/search/stock/US:spy/call/moneyness/in_the_money?ref_asset_price=450.5&limit=2&secret_key=your-secret-key&next_page_key=865eefd860dba1445d98c0368891bab8d3bd942aa3e988233cd470d6dbddc3f117df9c0108f411f25f06790745e356ba7417bf9eeb82ec14c808abcd16daf3fbabc615c3444f9e604f5816d99e71166d",
    "expiration_datetimes": [
      "2025-09-19T20:00:00Z"
    ],
    "data": {
      "2025-09-19T20:00:00Z": [
        {
          "instrument_id": 11400147,
          "asset_id": 863,
          "symbol": "SPY250919C00450000",
          "country_iso_code": "US",
          "exchange": "ARCX",
          "underlying_name": "SPY",
          "calendar_key": "US_STOCK",
          "session_template": "US_STOCK_RTH",
          "trading_codes": null,
          "is_indices": false,
          "status": "inactive",
          "parent_schema_instrument_id": "stock_100862",
          "daily_minute_count": 390,
          "contract_type": null,
          "contract_value": 100,
          "price_precision": null,
          "quantity_precision": null,
          "min_initial_open_quantity": null,
          "tick_size": null,
          "lot_size": null,
          "listing_date": null,
          "option_exchange": "BATO",
          "parent_asset_schema": "stock",
          "strike_price": 450,
          "expiration_date": "2025-09-19",
          "expiration_datetime": "2025-09-19T20:00:00+00:00",
          "option_type": "call",
          "exercise_style": "american"
        },
        {
          "instrument_id": 11400144,
          "asset_id": 863,
          "symbol": "SPY250919C00445000",
          "country_iso_code": "US",
          "exchange": "ARCX",
          "underlying_name": "SPY",
          "calendar_key": "US_STOCK",
          "session_template": "US_STOCK_RTH",
          "trading_codes": null,
          "is_indices": false,
          "status": "inactive",
          "parent_schema_instrument_id": "stock_100862",
          "daily_minute_count": 390,
          "contract_type": null,
          "contract_value": 100,
          "price_precision": null,
          "quantity_precision": null,
          "min_initial_open_quantity": null,
          "tick_size": null,
          "lot_size": null,
          "listing_date": null,
          "option_exchange": "BATO",
          "parent_asset_schema": "stock",
          "strike_price": 445,
          "expiration_date": "2025-09-19",
          "expiration_datetime": "2025-09-19T20:00:00+00:00",
          "option_type": "call",
          "exercise_style": "american"
        }
      ]
    }
  }
}
```

## Pagination

When the result set exceeds the number specified by the `limit` parameter, the response includes a `next_page_key` that can be used to retrieve the next set of results. To fetch the next page, include the `next_page_key` in your next request. Alternatively, you can directly use the `next_page_url` provided in the response.

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

# Search for in-the-money call options
options_params = {
    "schema_asset": SchemaAsset.STOCK,
    "country_symbol": "US:SPY",
    "option_type": "call",
    "moneyness": "in_the_money",
    "ref_asset_price": 450.5,
    "limit": 10
}

options = client.reference.search_option(**options_params)
print(options)

# Using more filter conditions
filtered_options_params = {
    "schema_asset": SchemaAsset.STOCK,
    "country_symbol": "US:SPY",
    "option_type": "put",
    "moneyness": "out_of_the_money",
    "ref_asset_price": 450.5,
    "strike_price": 440,
    "expiration_date": "2025-12-19",
    "limit": 5
}

filtered_options = client.reference.search_option(**filtered_options_params)
print(filtered_options)
```

## Notes

1. For the `moneyness` parameter:
   - `in_the_money`: For call options, strike price is below current price; for put options, strike price is above current price
   - `out_of_the_money`: For call options, strike price is above current price; for put options, strike price is below current price

2. If `ref_asset_price` is not provided, the API will use the latest price of the underlying asset to determine the moneyness of the options.

3. Option data in the response is grouped by expiration date, with each expiration date containing a list of options.
