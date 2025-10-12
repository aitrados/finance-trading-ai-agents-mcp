---
weight: 33
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Economic Event"
toc: true
description: "Retrieve a single economic calendar event"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Economic", "Calendar", "Event"]
---

## Economic Event Endpoint

Retrieve a single economic calendar event with detailed information.

### Endpoint URL

```
GET /api/v2/economic_calendar/event
```

### Description

This endpoint allows users to retrieve a single economic calendar event based on the provided query parameters. This is useful when you need to get specific details about a particular economic event such as GDP announcement, inflation report, or central bank decision.

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
| `sort` | string | No | "desc" | Sort direction ("asc" or "desc") |

## Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("ok" or "error") |
| `code` | integer | HTTP status code |
| `message` | string | Status message |
| `reference` | string | Reference ID (null if not applicable) |
| `result` | object | Contains the economic event data |

### Economic Event Fields

| Field | Type | Description                                                  |
|-------|------|--------------------------------------------------------------|
| `country_iso_code` | string | ISO country code                                             |
| `event_code` | string | Code representing the type of economic event                 |
| `event_name` | string | Human-readable name of the event                             |
| `event_driven_type` | string | Type of event ("time_driven" or "data_driven")                   |
| `importance` | integer | Numeric importance level (typically 1-3, where 3 is highest) |
| `impact` | string | Text representation of importance ("low", "medium", "high")  |
| `event_timestamp` | string | Date and time of the event in ISO format                     |
| `actual_value` | number | Actual value reported for the event                          |
| `previous_value` | number | Previous period's value                                      |
| `forecast_value` | number | Forecasted value before the event                            |
| `change` | number | Absolute change from previous value                          |
| `change_percent` | number | Percentage change from previous value                        |
| `period` | string | Period covered by the data (e.g., "Jul", "Q2")               |
| `unit` | string | Unit of measurement for the values                           |
| `source_id` | string | Unique identifier for the data source                        |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event?country_iso_code=US&event_code=GDP_GROWTH_RATE_QOQ&from_date=2025-01-01&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "country_iso_code": "FR",
    "event_code": "BUSINESS_PMI_SERVICES_HCOB",
    "event_name": "HCOB Services PMI",
    "event_driven_type": "time_driven",
    "importance": 3,
    "impact": "high",
    "event_timestamp": "2024-08-05T07:50:00Z",
    "actual_value": 50.1,
    "previous_value": 49.6,
    "forecast_value": 50.7,
    "change": 0.5,
    "change_percent": 0.0,
    "period": "Jul",
    "unit": "N/A",
    "source_id": "6cc0ae19fcdcf8f49375da5e88d8945cb495975131619c4d4253ebb52d1a3427"
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

# Get the most recent economic event (default behavior)
latest_event = client.economic.event()


# Get a specific economic event by country and event code
us_gdp = client.economic.event(
    country_iso_code="US",
    event_code="GDP_GROWTH_RATE_QOQ"
)
some_event = client.economic.event(
    source_id="6cc0ae19fcdcf8f49375da5e88d8945cb495975131619c4d4253ebb52d1a3427"
)


```

## Notes

1. This endpoint is particularly useful when you need to retrieve detailed information about a specific economic event, such as a GDP release, inflation report, or central bank decision.

2. While the endpoint can return any economic event that matches your query parameters, it's typically used to retrieve the most recent occurrence of a specific event by providing both `country_iso_code` and `event_code`.

3. The `importance` field (1-3) and `impact` field ("low", "medium", "high") help identify the potential market impact of the event. Events with an importance of 3 or "high" impact typically have the most significant market influence.

4. For economic analysis, it's valuable to compare the `actual_value` against both the `forecast_value` (market expectations) and `previous_value` (trend). Significant deviations between actual and forecast values often trigger market volatility.

5. The `source_id` parameter allows you to retrieve a specific event instance when you know its unique identifier. This is useful for tracking or referencing specific data points in your applications.

6. The `event_timestamp` field provides the exact date and time when the economic data was released or the event occurred. This is crucial for time-sensitive trading strategies that need to react to economic announcements.

7. Many economic indicators follow regular release schedules. For example, US Non-Farm Payrolls are typically released on the first Friday of each month. Understanding these patterns can help you anticipate and prepare for important economic events.

8. When using the date range parameters (`from_date` and `to_date`), the endpoint will return the most recent event within that range that matches your other filter criteria.
