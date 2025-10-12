---
weight: 31
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Holiday List"
toc: true
description: "Get holiday list information"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Holiday", "Calendar"]
---

## Holiday List Endpoint

Get holiday list information for a specific market or country.

### Endpoint URL

```
GET /api/v2/holiday/list
```

### Description

This endpoint allows users to obtain holiday list information for a specific market or country. You can retrieve holiday information by providing date ranges, holiday codes, and other filtering criteria.

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `full_symbol` | string | Yes | - | [Full symbol format](/docs/api/terminology/full_symbol/) to specify market or instrument, e.g., "STOCK:US:*" |
| `holiday_code` | string | No | - | Holiday code for filtering specific holidays |
| `from_date` | datetime | No | - | Start date for filtering events |
| `to_date` | datetime | No | - | End date for filtering events |
| `sort` | string | No | "asc" | Sort direction ("asc" or "desc") |
| `limit` | integer | No | 100 | Number of results to return (default 100, max 1001) |
| `format` | string | No | "csv" | Data format ("json" or "csv") |
| `next_page_key` | string | No | null | Pagination key for fetching next page of results |
| `secret_key` | string | Yes | - | Your API key |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | object | Result object |

### Result Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `next_page_key` | string | Key for fetching the next page of results |
| `next_page_url` | string | Complete URL for fetching the next page |
| `count` | integer | Number of results in the current response |
| `data` | array | Array of holiday information |

### Holiday Information Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Holiday name |
| `holiday_code` | string | Holiday code |
| `calendar_date` | string | Calendar date (YYYY-MM-DD format) |
| `asset_name` | string | Asset class name |
| `country_iso_code` | string | Country ISO code |
| `symbol` | string | Symbol or wildcard |
| `priority` | integer | Priority |
| `session_template` | string | Session template (e.g., "CLOSED") |
| `open_timestamp` | string | Market open timestamp (if applicable) |
| `close_timestamp` | string | Market close timestamp (if applicable) |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/holiday/list?full_symbol=stock%3AUS%3A%2A&from_date=2023-01-01+00%3A00%3A00&to_date=2026-12-31+00%3A00%3A00&sort=asc&limit=2&format=json&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "next_page_key": "250cae5532b463127d2a81a0b5ee9856da0cc338652751b1f6359ec2a59eea33",
    "next_page_url": "https://default.dataset-api.aitrados.com/api/v2/holiday/list?full_symbol=stock%3AUS%3A%2A&from_date=2023-01-01+00%3A00%3A00&to_date=2026-12-31+00%3A00%3A00&sort=asc&limit=2&format=json&secret_key=your-secret-key&next_page_key=250cae5532b463127d2a81a0b5ee9856da0cc338652751b1f6359ec2a59eea33",
    "count": 2,
    "data": [
      {
        "name": "New Year's Day",
        "holiday_code": "HOLIDAY_NEW_YEAR",
        "calendar_date": "2023-01-02",
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "*",
        "priority": 1,
        "session_template": "CLOSED",
        "open_timestamp": null,
        "close_timestamp": null
      },
      {
        "name": "Martin Luther King, Jr. Day",
        "holiday_code": "HOLIDAY_MLK_DAY",
        "calendar_date": "2023-01-16",
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "*",
        "priority": 1,
        "session_template": "CLOSED",
        "open_timestamp": null,
        "close_timestamp": null
      }
    ]
  }
}
```

## Code Examples

### Python

```python
import os
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient

config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)
client = DatasetClient(config=config)
# Get holiday list
for holiday_list in client.holiday.holiday_list(full_symbol="stock:US:*", from_date="2023-01-01", to_date="2026-12-31", limit=100):
    print(holiday_list)
```

## Notes

1. Using the wildcard `*` allows you to retrieve holiday information for all instruments in a specific market or asset class, such as `STOCK:US:*` for all US stock market holidays.

2. The `session_template` field indicates how the holiday affects trading sessions, e.g., "CLOSED" means the market is completely closed.

3. When retrieving large amounts of data using pagination, you can use the `next_page_key` or `next_page_url` from the response to fetch the next page of results.

4. Holiday information is crucial for building trading strategies, risk management, and settlement date calculations, helping you properly handle non-trading days.

5. The API supports holiday information for multiple countries and regions, use the appropriate country ISO code for filtering.

6. You can combine this endpoint with the holiday codes endpoint to get more detailed information about holiday codes.
#