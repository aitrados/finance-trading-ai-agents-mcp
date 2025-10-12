---
weight: 100
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Economic Calendar department"
icon: "event"
toc: true
description: "Macro data query based on the economic calendar: event codes, future events, latest occurred events (adapted for MCP tool calls)."
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["Economic Calendar","Economic Calendar MCP", "Macro", "Fundamental", "MCP", "LLM"]
---

The Economic Calendar module focuses on important macroeconomic events of major global economies (such as Non-Farm Payrolls, CPI, PMI, interest rate decisions, etc.). It supports retrieving future and historical data by country and event type, suitable for pre-strategy filtering, risk control, and news-driven trading.

Tip: Before use, please complete the Quickstart or ensure the service is running, and configure `AITRADOS_SECRET_KEY` in your `.env` file.
## API Data Source
https://docs.aitrados.com/en/docs/api/economic_event/event_codes/

## Available MCP Tools
- get_economic_calendar_event_codes
  - Purpose: To query available event codes for a specified country (providing codes for subsequent precise filtering).
  - Core parameter: `country_iso_code` (e.g., US, CN, GB, JP, etc.).
- get_upcoming_economic_calendar_event_list
  - Purpose: To query upcoming economic events.
  - Core parameters: `country_iso_code`, `event_code` (optional, from the previous tool), `impact` (HIGH/MEDIUM/LOW/ALL), `format` (csv/json), `limit` (1-100).
- get_latest_economic_calendar_event_list
  - Purpose: To query recently released economic events (recent history).
  - Core parameters: Same as above, with `date_type` set to `historical` internally.

## Quick Examples
- Querying available event codes for a country (LLM prompt example):
  Please call get_economic_calendar_event_codes with country_iso_code="US" and return all codes.

- Querying future high-impact events (Python/MCP client)
  country_iso_code="US", impact="HIGH", limit=5, format="csv"

- Fetching recently announced CPI-related events (first find the code, then filter)
  1) get_economic_calendar_event_codes(country_iso_code="US")
  2) Select the corresponding `event_code` for CPI from the results
  3) get_latest_economic_calendar_event_list(country_iso_code="US", event_code="CPI", limit=5)

## Return Data and Format
- Supports CSV and JSON. If feeding to an LLM, CSV is recommended to reduce context usage.
- A friendly message will be returned when no data is available (e.g., 'No upcoming economic calendar events found').

## Best Practices
- Event Foresight: Combine `get_upcoming` with `impact=HIGH` to schedule risk control windows in advance.
- Event Review: Use `latest` to retrieve actual values and compare them with previous and forecasted values for model calibration and review.
- Precise Filtering: Always fetch the list of event codes first, then use the `event_code` for precise queries.

## Add Custom Function Tools
- [Append custom function tools to the current MCP server](../custom_function_tool.md)

For more on running and environment configuration, please see the Quickstart.