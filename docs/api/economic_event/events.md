---
weight: 32
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Economic Event List"
toc: true
description: "Retrieve a list of economic calendar events"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Economic", "Calendar", "Events"]
---

## Economic Event List Endpoint

Retrieve a comprehensive list of economic calendar events with detailed information.

### Endpoint URL

```
GET /api/v2/economic_calendar/event_list
```

### Description

This endpoint allows users to retrieve a list of economic calendar events with filtering options by country, event code, date range, and other parameters. The events include important economic indicators, central bank decisions, and other significant economic announcements that impact financial markets.

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secret_key` | string | Yes | - | Your API key (min length 20) |
| `country_iso_code` | string | No | - | Country ISO code (e.g., "US", "CN", "UK", "EU", "DE", "FR", "JP", "AU", "CA", "CH", "HK") |
| `event_code` | string | No | - | Specific event code to filter by |
| `source_id` | string | No | - | Source ID (length 64) |
| `from_date` | datetime | No | - | Start date for filtering events (YYYY-MM-DD format) |
| `to_date` | datetime | No | - | End date for filtering events (YYYY-MM-DD format) |
| `sort` | string | No | "asc" | Sort direction ("asc" or "desc") |
| `limit` | integer | No | 100 | Number of results to return (default 100, max 1001) |
| `format` | string | No | "csv" | Data format ("json" or "csv") |
| `next_page_key` | string | No | - | Key for pagination to retrieve the next set of results |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | object | Contains the economic events data and pagination information |

### Result Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `next_page_key` | string | Key for retrieving the next page of results |
| `next_page_url` | string | Complete URL for the next page of results |
| `count` | integer | Number of records in the current response |
| `data` | array | Array of economic event records |

### Economic Event Fields

| Field | Type | Description |
|-------|------|-------------|
| `country_iso_code` | string | ISO country code |
| `event_code` | string | Code representing the type of economic event |
| `event_name` | string | Human-readable name of the event |
| `event_driven_type` | string | Type of event ("time_driven" or "data_driven") |
| `importance` | integer | Numeric importance level (typically 1-3, where 3 is highest) |
| `impact` | string | Text representation of importance ("low", "medium", "high") |
| `event_timestamp` | string | Date and time of the event in ISO format |
| `actual_value` | number | Actual value reported for the event |
| `previous_value` | number | Previous period's value |
| `forecast_value` | number | Forecasted value before the event |
| `change` | number | Absolute change from previous value |
| `change_percent` | number | Percentage change from previous value |
| `period` | string | Period covered by the data (e.g., "Jul", "Q2") |
| `unit` | string | Unit of measurement for the values |
| `source_id` | string | Unique identifier for the data source |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event_list?country_iso_code=US&limit=100&format=json&limit=2&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "next_page_key": "c6a6bee7ed83630b8910c294acf1978e215096d495a451873ccbc0d2b9bed4d8",
    "next_page_url": "https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event_list?country_iso_code=US&sort=asc&limit=100&format=json&limit=2&secret_key=your-secret-key&next_page_key=c6a6bee7ed83630b8910c294acf1978e215096d495a451873ccbc0d2b9bed4d8",
    "count": 2,
    "data": [
      {
        "country_iso_code": "US",
        "event_code": "BUSINESS_PMI_NON_MANUFACTURING_ISM",
        "event_name": "ISM Non-Manufacturing PMI",
        "event_driven_type": "time_driven",
        "importance": 3,
        "impact": "high",
        "event_timestamp": "2024-08-05T13:00:00Z",
        "actual_value": 51.4,
        "previous_value": 48.8,
        "forecast_value": 51.4,
        "change": 2.6,
        "change_percent": 0.0,
        "period": "Jul",
        "unit": "N/A",
        "source_id": "460b29c68f3590c1a6500b719cf9b4fc41f16b09d3ebb2a6c337fe41c1a75040"
      },
      {
        "country_iso_code": "US",
        "event_code": "BUSINESS_PMI_NON_MANUFACTURING_PRICES_ISM",
        "event_name": "ISM Non-Manufacturing Prices",
        "event_driven_type": "time_driven",
        "importance": 3,
        "impact": "high",
        "event_timestamp": "2024-08-05T13:00:00Z",
        "actual_value": 57.0,
        "previous_value": 56.3,
        "forecast_value": 56.0,
        "change": 0.7,
        "change_percent": 0.0,
        "period": "Jul",
        "unit": "N/A",
        "source_id": "2189bd77ba5a7b278a60b0128fa6b609ba65f13cad7c699d065fe655e5a510af"
      }
    ]
  }
}
```

## Code Example

### Python

```python
import os
from datetime import datetime, timedelta
from aitrados_api import ClientConfig
from aitrados_api import DatasetClient

config = ClientConfig(
    secret_key=os.getenv("AITRADOS_SECRET_KEY","YOUR_SECRET_KEY"),
)

client = DatasetClient(config=config)

# Get economic event list for US

for event_list in  client.economic.event_list(country_iso_code="US"):
    print(event_list)


# Get economic events with specific event code (e.g., inflation rate)
for event_list in  client.economic.event_list(
    country_iso_code="US",
    event_code="INFLATION_RATE_HEADLINE_YOY",
    limit=10
):
    print(event_list)


```

## Notes

1. The `importance` field (numeric value 1-3) and `impact` field (text "low", "medium", "high") help identify which events are likely to have the most significant market impact. High importance events (importance=3) are typically major releases like GDP, inflation, or central bank decisions.

2. The `event_driven_type` field distinguishes between regularly scheduled economic releases ("time_driven") and events that occur in response to specific conditions.

3. The `change` and `change_percent` fields help quickly identify the magnitude and direction of change in an economic indicator compared to its previous reading.

4. For comprehensive market analysis, it's valuable to compare the `actual_value` against both the `forecast_value` (market expectations) and `previous_value` (trend). Significant deviations between actual and forecast values often trigger market volatility.

5. The `period` field indicates the time period covered by the data (e.g., month, quarter). This is important for contextualizing the data, especially for seasonal indicators.

6. Using the `next_page_key` parameter enables efficient pagination through large datasets when the number of events exceeds the limit parameter.

7. The `source_id` field provides a unique identifier for the data source, which can be useful for tracking or referencing specific data points in your applications.

8. When analyzing economic events across multiple countries, consider using the ISO country codes to systematically retrieve and compare data across different economies.
