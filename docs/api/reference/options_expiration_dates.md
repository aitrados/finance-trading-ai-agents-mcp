---
weight: 21
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Options Expiration Dates"
toc: true
description: "Get a list of option expiration dates for a specific asset"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Options","option expiration dates"]
---

## Options Expiration Dates Endpoint

Get a list of option expiration dates for a specific asset.

### Endpoint URL

```
GET /api/v2/option/expiration_date_list/{schema_asset}/{country_symbol}
```

### Description

This endpoint allows users to get a list of option expiration dates for a specific asset. Each expiration date includes a date string and a complete datetime in ISO 8601 format.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schema_asset` | string | Yes | Asset type, see [Asset Types](/docs/api/terminology/asset_name/) |
| `country_symbol` | string | Yes | Country and symbol format, see [Country Symbol](/docs/api/terminology/country_symbol/) |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secret_key` | string | Yes | - | Your API key |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | array | Array of expiration dates |

### Expiration Date Fields

| Field | Type | Description |
|-------|------|-------------|
| `expiration_date` | string | Expiration date (date format) |
| `expiration_datetime` | string | Expiration datetime (ISO 8601 format) |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/stock/US:SPY&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": "cached",
  "result": [
    {
      "expiration_date": "2025-09-19",
      "expiration_datetime": "2025-09-19T20:00:00+00:00"
    },
    {
      "expiration_date": "2025-09-30",
      "expiration_datetime": "2025-09-30T20:00:00+00:00"
    },
    {
      "expiration_date": "2025-10-17",
      "expiration_datetime": "2025-10-17T20:00:00+00:00"
    },
    {
      "expiration_date": "2025-10-31",
      "expiration_datetime": "2025-10-31T20:00:00+00:00"
    },
    {
      "expiration_date": "2025-11-21",
      "expiration_datetime": "2025-11-21T21:00:00+00:00"
    }
  ]
}
```

## Code Example

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

# Get options expiration date list for specific asset
expiration_date_list = client.reference.options_expiration_date_list(
    schema_asset=SchemaAsset.STOCK, 
    country_symbol="US:SPY", 
)
print(expiration_date_list)

# Access the first expiration date in the results
if expiration_date_list and "result" in expiration_date_list and len(expiration_date_list["result"]) > 0:
    first_date = expiration_date_list["result"][0]
    print(f"Nearest option expiration date: {first_date['expiration_date']}")
```

## Notes

1. The list of expiration dates returned by this endpoint is arranged in chronological order, starting with the nearest expiration date.

2. Before retrieving option contracts, you can use this endpoint to get valid expiration dates, then use it with the [Options Search Endpoint](/docs/api/reference/search_options/) to retrieve option contracts for specific expiration dates.

3. For some assets, long-term expiration dates (LEAPS) may be returned, which can extend several years into the future.

4. Timezone information is included in the `expiration_datetime` field in ISO 8601 format.

