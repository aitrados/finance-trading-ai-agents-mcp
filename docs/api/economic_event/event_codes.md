---
weight: 30
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Economic Event Codes"
toc: true
description: "Retrieve economic calendar event codes by country"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "Economic", "Calendar"]
---

## Economic Event Codes Endpoint

Retrieve economic event codes for a specific country.

### Endpoint URL

```
GET /api/v2/economic_calendar/event_codes/{country_iso_code}
```

### Description

This endpoint allows users to retrieve all available economic event codes for a specific country. These codes represent various economic indicators and events that are tracked in the economic calendar, such as GDP growth rates, inflation metrics, employment statistics, and central bank decisions.

## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description                                                                           |
|-----------|------|----------|---------------------------------------------------------------------------------------|
| `country_iso_code` | string | Yes | Country ISO code (e.g., "US",  "UK", "EU", "DE", "FR", "JP", "AU", "CA", "CH", "HK","CN") |

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
| `result` | object | Key-value pairs of event codes and their descriptions |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event_codes/US?secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "GDP_GROWTH_RATE_QOQ": "GDP Growth Rate QoQ",
    "GDP_ABSOLUTE_QOQ": "Gross Domestic Product QoQ",
    "INFLATION_CPI_NSA": "CPI",
    "INFLATION_CPI_SA": "CPI s.a",
    "INFLATION_RATE_HEADLINE_MOM": "Inflation Rate MoM",
    "INFLATION_RATE_HEADLINE_YOY": "Inflation Rate YoY",
    "INFLATION_RATE_CORE_MOM": "Core Inflation Rate MoM",
    "INFLATION_RATE_CORE_YOY": "Core Inflation Rate YoY",
    "INFLATION_PPI_HEADLINE_MOM": "Producer Price Index MoM",
    "INFLATION_PCE_CORE_MOM": "Core PCE Price Index MoM",
    "INFLATION_PCE_CORE_YOY": "Core PCE Price Index YoY",
    "EMPLOYMENT_UNEMPLOYMENT_RATE_U3": "Unemployment Rate",
    "EMPLOYMENT_UNEMPLOYMENT_RATE_U6": "U-6 Unemployment Rate",
    "EMPLOYMENT_NFP_HEADLINE": "Non Farm Payrolls",
    "EMPLOYMENT_NFP_PRIVATE": "Nonfarm Payrolls Private",
    "EMPLOYMENT_ADP_PRIVATE_CHANGE": "ADP Employment Change",
    "EMPLOYMENT_INITIAL_JOBLESS_CLAIMS": "Initial Jobless Claims",
    "EMPLOYMENT_CONTINUING_JOBLESS_CLAIMS": "Continuing Jobless Claims",
    "EMPLOYMENT_JOBLESS_CLAIMS_4WK_AVG": "Jobless Claims 4-Week Average",
    "EMPLOYMENT_JOLTS_JOB_OPENINGS": "JOLTs Job Openings",
    "CONSUMPTION_RETAIL_SALES_HEADLINE_MOM": "Retail Sales MoM",
    "CONSUMPTION_RETAIL_SALES_HEADLINE_YOY": "Retail Sales YoY",
    "CONSUMPTION_RETAIL_SALES_EX_AUTOS_MOM": "Retail Sales Ex Autos MoM",
    "CONSUMPTION_RETAIL_SALES_EX_GAS_AUTOS_MOM": "Retail Sales Ex Gas/Autos MoM",
    "CONSUMPTION_PERSONAL_INCOME_MOM": "Personal Income MoM",
    "CONSUMPTION_PERSONAL_SPENDING_MOM": "Personal Spending MoM",
    "CONSUMPTION_SENTIMENT_MICHIGAN": "Michigan Consumer Sentiment",
    "BUSINESS_PMI_MANUFACTURING_ISM": "ISM Manufacturing PMI",
    "BUSINESS_PMI_SERVICES_ISM": "ISM Services PMI",
    "BUSINESS_PMI_NON_MANUFACTURING_ISM": "ISM Non-Manufacturing PMI",
    "BUSINESS_PMI_NON_MANUFACTURING_PRICES_ISM": "ISM Non-Manufacturing Prices",
    "BUSINESS_PMI_MANUFACTURING_SP_GLOBAL": "S&P Global Manufacturing PMI",
    "BUSINESS_PMI_SERVICES_SP_GLOBAL": "S&P Global Services PMI",
    "BUSINESS_DURABLE_GOODS_HEADLINE_MOM": "Durable Goods Orders MoM",
    "BUSINESS_DURABLE_GOODS_EX_DEFENSE_MOM": "Durable Goods Orders ex Defense MoM",
    "BUSINESS_DURABLE_GOODS_EX_TRANSPORT_MOM": "Durable Goods Orders Ex Transp MoM",
    "BUSINESS_MANUFACTURING_INDEX_NY_EMPIRE": "NY Empire State Manufacturing Index",
    "HOUSING_STARTS_ABSOLUTE": "Housing Starts",
    "HOUSING_BUILDING_PERMITS_ABSOLUTE": "Building Permits",
    "HOUSING_NEW_HOME_SALES_ABSOLUTE": "New Home Sales",
    "HOUSING_EXISTING_HOME_SALES_ABSOLUTE": "Existing Home Sales",
    "HOUSING_EXISTING_HOME_SALES_MOM": "Existing Home Sales MoM",
    "TRADE_BALANCE_GOODS": "Goods Trade Balance",
    "TRADE_BALANCE_OVERALL": "Balance of Trade",
    "FED_POLICY_INTEREST_RATE_DECISION": "Fed Interest Rate Decision",
    "FED_POLICY_FOMC_MINUTES": "FOMC Minutes",
    "FED_POLICY_FOMC_PROJECTIONS": "FOMC Economic Projections",
    "FED_POLICY_MONETARY_POLICY_REPORT": "Monetary Policy Report",
    "FED_SPEECH_POWELL": "Fed Chair Powell Speech",
    "FED_TESTIMONY_POWELL": "Fed Chair Powell Testimony",
    "FED_EVENT_PRESS_CONFERENCE": "Press Conference",
    "FED_EVENT_FOMC_PRESS_CONFERENCE": "Fed Press Conference",
    "BONDS_AUCTION_10_YEAR_NOTE": "10-Year Note Auction",
    "FED_EVENT_JACKSON_HOLE_SYMPOSIUM": "Jackson Hole Symposium",
    "POLITICAL_EVENT_PRESIDENTIAL_ELECTION": "Presidential Elections",
    "POLITICAL_EVENT_INAUGURATION_DAY": "Inauguration Day"
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

# Get economic event codes for a specific country (e.g., US)
us_event_codes = client.economic.event_codes(country_iso_code="US")
print(us_event_codes)

# Get economic event codes for China
uk_event_codes = client.economic.event_codes(country_iso_code="UK")
print(uk_event_codes)

# Print all available GDP-related event codes for the US
us_codes = client.economic.event_codes(country_iso_code="US")
if us_codes and "result" in us_codes:
    gdp_codes = {code: desc for code, desc in us_codes["result"].items() if code.startswith("GDP_")}
    print("Available GDP indicators:")
    for code, desc in gdp_codes.items():
        print(f"{code}: {desc}")

# Find all inflation-related events
us_codes = client.economic.event_codes(country_iso_code="US")
if us_codes and "result" in us_codes:
    inflation_codes = {code: desc for code, desc in us_codes["result"].items() if "INFLATION" in code}
    print("\nAvailable inflation indicators:")
    for code, desc in inflation_codes.items():
        print(f"{code}: {desc}")
```

## Notes

1. Event codes are organized by category, which is reflected in their naming convention (e.g., `GDP_`, `INFLATION_`, `EMPLOYMENT_`, etc.). This makes it easier to filter and find specific types of economic indicators.

2. Different countries may have different sets of available economic indicators. Some indicators are country-specific, while others are more universal.

3. These event codes can be used with the Economic Calendar Events endpoint to retrieve actual event data, including forecasts, actual values, and previous values for specific economic indicators.

4. Economic event codes are essential for constructing data-driven trading strategies based on economic announcements and their impact on financial markets.

5. The naming convention for event codes is standardized across the API, making it easier to programmatically work with specific categories of economic indicators.

6. For important economic indicators like GDP, inflation, and employment, multiple variations may be available (e.g., MoM vs YoY, headline vs core), allowing for more nuanced analysis.
