---
weight: 30
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Holiday Codes"
toc: true
description: "Get holiday codes for various countries"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Holiday", "Calendar"]
---

## Holiday Codes Endpoint

Get holiday codes for a specific country.

### Endpoint URL

```
GET /api/v2/holiday/holiday_codes/{country_iso_code}
```

### Description

This endpoint allows users to get all available holiday codes for a specific country. These codes represent the various holidays tracked in the holiday calendar, such as New Year's Day, Christmas, Independence Day, and other country or region-specific holidays.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|---------------------------------------------------------------------------------------|
| `country_iso_code` | string | Yes | Country ISO code (e.g., "US", "UK", "EU", "DE", "FR", "JP", "AU", "CA", "CH", "HK", "CN") |

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
| `result` | object | Key-value pairs of holiday codes and their descriptions |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/holiday/holiday_codes/US?secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "HOLIDAY_NEW_YEAR": "New Year's Day",
    "HOLIDAY_NEW_YEAR_EVE": "New Year's Eve",
    "HOLIDAY_CHRISTMAS": "Christmas Day",
    "HOLIDAY_CHRISTMAS_EVE": "Christmas Eve",
    "HOLIDAY_GOOD_FRIDAY": "Good Friday",
    "HOLIDAY_MEMORIAL_DAY": "Memorial Day",
    "HOLIDAY_INDEPENDENCE_DAY": "Independence Day",
    "HOLIDAY_LABOR_DAY": "Labor Day",
    "HOLIDAY_THANKSGIVING": "Thanksgiving Day",
    "HOLIDAY_PRESIDENTS_DAY": "Presidents' Day",
    "HOLIDAY_WASHINGTON_BIRTHDAY": "Washington's Birthday",
    "HOLIDAY_MLK_DAY": "Martin Luther King, Jr. Day",
    "HOLIDAY_JUNETEENTH": "Juneteenth",
    "HOLIDAY_NATIONAL_DAY_OF_MOURNING": "National Day of Mourning",
    "HOLIDAY_MOURNING_GHWB": "Mourning - In Honor Of George H.W. Bush"
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
holiday_codes= client.holiday.holiday_codes()

```

## Notes

1. Holiday codes are organized according to a unified naming convention (e.g., all codes begin with `HOLIDAY_`), making it easier to filter and find specific types of holidays.

2. Different countries may have different sets of holidays. Some holidays are country-specific, while others are more universal (such as New Year's Day, Christmas, etc.).

3. These holiday codes can be used with the holiday calendar events endpoint to get actual data for specific holidays, including dates and observances.

4. Holiday codes are crucial for building trading strategies that consider market closures, helping traders predict changes in market liquidity and volatility.

5. The API supports holiday information for multiple countries and regions, including the United States, China, European Union, United Kingdom, Germany, France, Japan, Australia, Canada, Switzerland, and Hong Kong.

6. Holiday information can be used for risk management, settlement date calculations, and other financial applications that need to consider non-trading days.
