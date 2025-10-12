---
weight: 21
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "Latest News List"
toc: true
description: "Get the most recent news information"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "News", "Real-time", "Market Data"]
---

## Latest News Endpoint

Get the most recent news related to specific assets or across all markets.

### Endpoint URL

```
GET /api/v2/news/latest
```

### Description

This endpoint allows users to retrieve the most recent news items related to specific assets or across all markets. Unlike the regular news list endpoint, this endpoint does not require date parameters and is optimized for real-time data access, making it ideal for applications that need the most up-to-date market news.

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `full_symbol` | string | No | - | [Full symbol format](/docs/api/terminology/full_symbol/) to specify an asset, e.g., "STOCK:US:TSLA" |
| `sort` | string | No | "asc" | Sort direction ("asc" or "desc") |
| `limit` | integer | No | 100 | Number of results to return (default 100, max 1001) |
| `secret_key` | string | Yes | - | Your API key |

## Response

### Response Fields

The response structure is identical to the [News List](/docs/api/news/news_list/) endpoint:

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
GET https://default.dataset-api.aitrados.com/api/v2/news/latest?full_symbol=stock%3AUS%3ATSLA&limit=2&secret_key=your-secret-key
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
        "sentiment_label": "neutral",
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-09-14T10:25:14+00:00",
        "publisher": "reuters.com",
        "title": "Tesla to unveil new charging technology next month",
        "text_content": "Tesla Inc is set to unveil its new fast-charging technology at an event next month, according to sources familiar with the matter. The technology could significantly reduce charging times for its electric vehicles.",
        "publisher_url": "https://www.reuters.com/business/autos-transportation/tesla-unveil-new-charging-technology-next-month-2025-09-14/",
        "sentiment_score": 0.1
      },
      {
        "sentiment_label": "positive",
        "asset_name": "stock",
        "country_iso_code": "US",
        "symbol": "TSLA",
        "link_type": "SPECIFIC_ASSET",
        "published_date": "2025-09-14T08:05:51+00:00",
        "publisher": "bloomberg.com",
        "title": "Tesla's Berlin Factory Reaches Production Milestone",
        "text_content": "Tesla's Berlin Gigafactory has reached a significant production milestone, manufacturing its 500,000th vehicle since opening. The achievement comes as the company continues to expand its European operations.",
        "publisher_url": "https://www.bloomberg.com/news/articles/2025-09-14/tesla-berlin-factory-reaches-production-milestone",
        "sentiment_score": 0.65
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

# Get latest news - useful for real-time data
news_latest = client.news.news_latest(full_symbol="stock:US:TSLA", limit=5)
print(news_latest)
```

## Notes

1. This endpoint is optimized for retrieving the most recent news and is ideal for real-time applications or dashboards that need to display the latest market information.

2. Unlike the regular news list endpoint, this endpoint does not require date range parameters (`from_date` and `to_date`), making it simpler to use for real-time data access.

3. The `full_symbol` parameter is optional. If provided, the API will return the latest news related to the specified asset; if not provided, the API will return the latest news across all markets.

4. The response structure is similar to the news list endpoint but does not include pagination-related fields (`next_page_key` and `next_page_url`) as this endpoint is designed to provide only the most recent news items.

5. Sentiment analysis fields (`sentiment_label` and `sentiment_score`) can help quantify the potential market impact of recent news, which is particularly valuable for real-time trading decisions.

6. For historical news analysis or when you need to retrieve news from a specific time period, use the [News List](/docs/api/news/news_list/) endpoint instead.

    ],
)

