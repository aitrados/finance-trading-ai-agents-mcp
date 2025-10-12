---
weight: 35
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Economic Latest Events"
toc: true
description: "Retrieve recent economic calendar events with flexible time filtering"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Economic", "Calendar", "Events","Latest Event", "Upcoming", "Historical"]
---

## Economic Latest Events Endpoint

Retrieve the most recent economic calendar events with flexible time-based filtering to access upcoming, historical, or all recent events.

### Endpoint URL


```
GET /api/v2/economic_calendar/latest_event_list
```

### Description

This endpoint provides access to the most recent economic calendar events with powerful time-based filtering capabilities. Unlike the general event list endpoint, this specialized endpoint focuses on retrieving recent events around the current time period, making it ideal for real-time financial decision-making and market analysis.

**Key Features:**
- **Upcoming Events**: Access future economic events to prepare for market-moving announcements
- **Historical Events**: Retrieve recently concluded events to analyze their market impact
- **Combined View**: Get both recent historical and upcoming events for comprehensive market context
- **Financial Decision Support**: Optimized for traders and analysts who need timely economic data

This functionality is particularly valuable for guiding financial operations as it provides immediate access to the economic events that are most relevant to current market conditions.

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description                                                                               |
|-----------|------|----------|---------|-------------------------------------------------------------------------------------------|
| `secret_key` | string | Yes | -       | Your API key (min length 20)                                                              |
| `country_iso_code` | string | No | -       | Country ISO code (e.g., "US", "CN", "UK", "EU", "DE", "FR", "JP", "AU", "CA", "CH", "HK") |
| `event_code` | string | No | -       | Specific event code to filter by                                                          |
| `date_type` | string | No | "all"   | **Core Parameter**: Controls time filtering - "upcoming" (future events), "historical" (recent past events), or "all" (both upcoming and recent historical events) |
| `sort` | string | No | "asc"   | Sort direction ("asc" or "desc")                                                          |
| `limit` | integer | No | 5       | Number of results to return (default 5, max 1001)                                         |
| `format` | string | No | "csv"   | Data format ("json" or "csv")                                                             |

### Date Type Parameter Details

The `date_type` parameter is the core functionality of this endpoint:

- **"upcoming"**: Returns future economic events that haven't occurred yet
- **"historical"**: Returns recently concluded economic events  
- **"all"**: Returns both recent historical and upcoming events (combines the above two)

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
GET https://default.dataset-api.aitrados.com/api/v2/economic_calendar/latest_event_list?country_iso_code=us&date_type=upcoming&limit=5&format=json&&secret_key=your-secret-key
```

## Response Example

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

# Get economic latest event list
latest_events = client.economic.latest_events(country_iso_code="us",date_type="upcoming")
print(latest_events)


```



## Use Cases and Benefits

### 1. **Pre-Market Analysis** 
Use `date_type="upcoming"` to identify market-moving events scheduled for the day or week ahead, allowing traders to position themselves appropriately.

### 2. **Post-Event Impact Assessment**
Use `date_type="historical"` to analyze recently concluded events and their potential ongoing market effects.

### 3. **Comprehensive Market Context**
Use `date_type="all"` to get both historical context and upcoming events in a single request, providing a complete picture around the current time period.

### 4. **Real-Time Trading Support**
The focused nature of this endpoint makes it ideal for real-time trading applications where you need quick access to the most relevant economic events.

### 5. **Risk Management**
By knowing both recent outcomes and upcoming events, traders can better manage portfolio risk around high-impact economic announcements.

## Notes

1. **Time Relevance**: This endpoint is optimized for recent events around the current time, making it more suitable for active trading and real-time analysis compared to the general event list endpoint.

2. **Financial Decision Making**: The `date_type` parameter's flexibility makes this endpoint particularly valuable for financial operations, as it provides exactly the temporal perspective needed for different trading strategies.

3. **Market Impact Focus**: Recent and upcoming events typically have the most significant impact on current market conditions, making this endpoint ideal for traders and analysts focused on immediate market movements.

4. **Efficiency**: By limiting results to recent timeframes, this endpoint provides faster response times and more focused data sets compared to broader historical queries.

5. **Event Timing**: Pay special attention to the `event_timestamp` field when using `date_type="all"` to distinguish between historical and upcoming events in the combined results.

6. **Strategy Applications**: 
   - Use "upcoming" for preparation and positioning strategies
   - Use "historical" for impact analysis and post-mortem evaluation
   - Use "all" for comprehensive market context and correlation analysis
