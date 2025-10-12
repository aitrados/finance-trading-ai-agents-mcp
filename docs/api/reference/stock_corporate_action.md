---
weight: 22
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Stock Corporate Actions"
toc: true
description: "Get corporate actions (dividends, splits) for a specific stock"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Stocks"]
---

## Stock Corporate Actions Endpoint

Get corporate actions (dividends, splits) for a specific stock.

### Endpoint URL

```
GET /api/v2/stock/stock_corporate_action/list/{country_symbol}
```

### Description

This endpoint allows users to retrieve corporate actions such as dividends and stock splits for a specific stock. The data includes detailed information about each corporate action including dates, adjustment factors, and cash amounts.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_symbol` | string | Yes | Country and symbol format (e.g., "US:TSLA"), see [Country Symbol](/docs/api/terminology/country_symbol/) |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secret_key` | string | Yes | - | Your API key |
| `from_date` | datetime | Yes | - | Start date in YYYY-MM-DD format |
| `to_date` | datetime | No | - | End date in YYYY-MM-DD format |
| `action_type` | string | No | - | Type of corporate action: 'dividend' or 'split' |
| `format` | string | No | "json" | Data format ("json" or "csv") |
| `limit` | integer | No | 150 | Number of results to return (default 150, max 1000) |
| `next_page_key` | string | No | - | Key for pagination to retrieve the next set of results |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | object | Contains the corporate actions data and pagination information |

### Result Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `next_page_key` | string | Key for retrieving the next page of results |
| `next_page_url` | string | Complete URL for the next page of results |
| `count` | integer | Number of records in the current response |
| `data` | array | Array of corporate action records |

### Corporate Action Fields

| Field | Type | Description |
|-------|------|-------------|
| `asset_schema` | string | Asset type (e.g., "STOCK") |
| `country_iso_code` | string | ISO country code |
| `symbol` | string | Stock ticker symbol |
| `exchange` | string | Exchange code |
| `action_type` | string | Type of corporate action ("dividend" or "split") |
| `ex_date` | string | Ex-dividend or ex-split date |
| `adjustment_factor` | string | Price adjustment factor |
| `cash_amount` | number | Cash amount for dividends (null for splits) |
| `currency` | string | Currency code for cash amount (null for splits) |
| `declaration_date` | string | Date when the corporate action was announced |
| `record_date` | string | Date used to determine eligible shareholders |
| `pay_date` | string | Date when dividends are paid or splits take effect |
| `split_from` | integer | Original number of shares (for splits) |
| `split_to` | integer | New number of shares (for splits) |
| `reference_price` | number | Reference price for the action (if available) |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/stock/stock_corporate_action/list/US:TSLA?from_date=2020-08-18&action_type=split&format=json&limit=1&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "next_page_key": "98aef725d40f84a833b65eba1627c018a26ba1b3112b0c825cbde9f9b4513941",
    "next_page_url": "https://default.dataset-api.aitrados.com/api/v2/stock/stock_corporate_action/list/US:TSLA?from_date=2020-08-18+00%3A00%3A00&action_type=split&format=json&limit=1&secret_key=your-secret-key&next_page_key=98aef725d40f84a833b65eba1627c018a26ba1b3112b0c825cbde9f9b4513941",
    "count": 1,
    "data": [
      {
        "asset_schema": "STOCK",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "exchange": "XNAS",
        "action_type": "split",
        "ex_date": "2020-08-31",
        "ex_date__1": "2020-08-31",
        "adjustment_factor": "0.20000000",
        "cash_amount": null,
        "currency": null,
        "declaration_date": null,
        "record_date": null,
        "pay_date": null,
        "split_from": 1,
        "split_to": 5,
        "reference_price": null
      }
    ]
  }
}
```

## Code Example

### Python

```python
import os
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient

config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)

client = DatasetClient(config=config)

# Get stock corporate action list
for actions in client.reference.stock_corporate_action_list(
    country_symbol="US:TSLA",
    from_date="2020-01-18",
    action_type="split",
    limit=100
):
    print(actions)



```

## Notes

1. Corporate actions data is critical for accurate historical price analysis and portfolio tracking.

2. Stock splits require price adjustment for historical comparisons. The `adjustment_factor` provides the multiplier needed to adjust prices before the split.

3. For stock splits, the `split_from` and `split_to` fields indicate the split ratio. For example, a 1:5 split (1 to 5) means that for each original share, shareholders received 5 new shares.

4. Dividend information includes the `ex_date` (when the stock begins trading without the dividend value), `record_date` (date used to determine eligible shareholders), and `pay_date` (when the dividend is actually paid).

5. Using pagination with `next_page_key` allows you to retrieve large datasets efficiently when the number of corporate actions exceeds the limit parameter.