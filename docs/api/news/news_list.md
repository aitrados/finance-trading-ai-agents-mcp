---
weight: 20
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "News List"
toc: true
description: "Get news list information"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "News", "Market Data"]
---

## News List Endpoint

Get a list of news related to specific assets or within a specified time range.

### Endpoint URL

```
GET /api/v2/news/list
```

### Description

This endpoint allows users to retrieve news items related to specific assets or all news within a specified time range. Each news item includes information such as title, content summary, publication time, publisher, and original link.

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `from_date` | datetime | Yes | - | Start date for filtering news |
| `to_date` | datetime | Yes | - | End date for filtering news |
| `full_symbol` | string | No | - | [Full symbol format](/docs/api/terminology/full_symbol/) to specify an asset, e.g., "STOCK:US:TSLA" |
| `sort` | string | No | "asc" | Sort direction ("asc" or "desc") |
| `limit` | integer | No | 100 | Number of results to return (default 100, max 1001) |
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
| `data` | array | Array of news information |

### News Information Fields

| Field | Type | Description |
|-------|------|-------------|
| `sentiment_label` | string | Sentiment label (may be null) |
| `asset_name` | string | Asset class name |
| `country_iso_code` | string | Country ISO code |
| `symbol` | string | Asset symbol |
| `link_type` | string | Link type (e.g., "SPECIFIC_ASSET") |
| `published_date` | string | Publication date and time (ISO 8601 format) |
| `publisher` | string | Publisher (news source) |
| `title` | string | News title |
| `text_content` | string | News content summary |
| `publisher_url` | string | Original news link |
| `sentiment_score` | float | Sentiment analysis score (may be null) |

## Request Example

```
GET https://default.dataset-api.aitrados.com/api/v2/news/list?from_date=2025-07-01+00%3A00%3A00&to_date=2025-12-31+00%3A00%3A00&full_symbol=stock%3AUS%3ATSLA&sort=asc&limit=100&secret_key=your-secret-key
```

## Response Example

```json
{
  "status": "ok",
  "code": 200,
  "message": "success",
  "reference": null,
  "result": {
    "next_page_key": "921caf51346003d13bfc0249c172242a897dd88ed289bcbe8d851cbd09e6d76e",
    "next_page_url": "https://default.dataset-api.aitrados.com/api/v2/news/list?from_date=2025-07-01+00%3A00%3A00&to_date=2025-12-31+00%3A00%3A00&full_symbol=stock%3AUS%3ATSLA&sort=asc&limit=2&secret_key=your-secret-key&next_page_key=921caf51346003d13bfc0249c172242a897dd88ed289bcbe8d851cbd09e6d76e",
    "count": 2,
    "data": [
      {
        "sentiment_label": null,
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-07-01T02:57:14+00:00",
        "publisher": "reuters.com",
        "title": "Tesla registrations in Denmark fall 61.6% year-on-year in June",
        "text_content": "Tesla's registration of new cars in Denmark fell by 61.57% in June from the same month a year ago to 1,282 vehicles, registration data from Mobility Denmark showed on Tuesday.",
        "publisher_url": "https://www.reuters.com/business/autos-transportation/tesla-registrations-denmark-fall-616-year-on-year-june-2025-07-01/",
        "sentiment_score": null
      },
      {
        "sentiment_label": null,
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-07-01T03:49:51+00:00",
        "publisher": "reuters.com",
        "title": "Tesla sales drop over 60% in Sweden and Denmark",
        "text_content": "Tesla's sales dropped for a sixth straight month in Sweden and Denmark in June, underscoring the challenges the EV-maker faces as competitors gain market share and CEO Elon Musk's popularity declines.",
        "publisher_url": "https://www.reuters.com/business/autos-transportation/tesla-sales-drop-over-60-sweden-denmark-2025-07-01/",
        "sentiment_score": null
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
# Get news list
for news_list in client.news.news_list(full_symbol="stock:US:TSLA", from_date="2025-07-01", to_date="2025-12-31", limit=100):
    print(news_list)
```

## Notes

1. The time range parameters `from_date` and `to_date` are required to limit the number of news items returned. It is recommended to use a reasonable time range for optimal performance.

2. The `full_symbol` parameter is optional. If provided, the API will return news related to the specified asset; if not provided, the API will return all news within the time range.

3. Sentiment analysis fields `sentiment_label` and `sentiment_score` provide analysis of the news sentiment, which can be used to quantify the potential impact of news on the market. These fields may be null, indicating that sentiment analysis has not been performed.

4. The news content (`text_content`) is typically a summary or the first few paragraphs of the original news. For the full content, you can access the original news link via `publisher_url`.

5. When retrieving large amounts of data using pagination, you can use the `next_page_key` or `next_page_url` from the response to fetch the next page of results.

6. This API's data sources include multiple well-known financial news providers, such as Reuters, Bloomberg, etc., providing high-quality market-related news.
