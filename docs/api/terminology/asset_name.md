---
weight: 1
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Asset Names"
toc: true
description: "Reference for all supported asset types in the AiTrados API"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["Beginners", "API", "Python"]

---

## Asset Types Overview

AiTrados API supports multiple asset classes across global markets. This reference details all available asset types used in the `full_symbol` notation.

## Supported Asset Types

| Asset Type | Description | Example Full Symbol |
|------------|-------------|--------------------|
| `STOCK` | Equities including common stocks, ETFs, and indices | `STOCK:US:AAPL` |
| `FOREX` | Foreign exchange currency pairs | `FOREX:GLOBAL:EURUSD` |
| `CRYPTO` | Cryptocurrency pairs | `CRYPTO:GLOBAL:BTCUSDT` |
| `FUTURE` | Futures contracts | `FUTURE:US:ESU23` |
| `OPTION` | Options contracts | `OPTION:US:SPY250707C00450000` |

## STOCK

Represents equities traded on stock exchanges worldwide. This includes individual company stocks, ETFs (Exchange Traded Funds), and market indices.

**Markets Available**: US, JP, HK, CN, UK, DE, and others

**Example Usage**:
```python
# Query Apple Inc. stock data
params = {
    "full_symbol": "STOCK:US:AAPL",
    # Additional parameters
}
```

## FOREX

Represents foreign exchange currency pairs in the global forex market. Always uses the `GLOBAL` country designation.

**Markets Available**: GLOBAL

**Example Usage**:
```python
# Query EUR/USD exchange rate data
params = {
    "full_symbol": "FOREX:GLOBAL:EURUSD",
    # Additional parameters
}
```

## CRYPTO

Represents cryptocurrency trading pairs across various exchanges. Uses the `GLOBAL` country designation.

**Markets Available**: GLOBAL

**Example Usage**:
```python
# Query Bitcoin/USDT data
params = {
    "full_symbol": "CRYPTO:GLOBAL:BTCUSDT",
    # Additional parameters
}
```

## FUTURE

Represents futures contracts for commodities, indices, and other underlying assets.

**Markets Available**: US, UK, JP, and others

**Naming Convention**: Futures symbols typically include an expiration code, where:
- Letter represents the month (H=March, M=June, U=September, Z=December, etc.)
- Number represents the year (3=2023, 4=2024, etc.)

**Example Usage**:
```python
# Query E-mini S&P 500 futures for September 2023
params = {
    "full_symbol": "FUTURE:US:ESU23",
    # Additional parameters
}
```

## OPTION

Represents options contracts on stocks, indices, and other underlying assets.

**Markets Available**: US, and others

**Naming Convention**: Option symbols follow a standardized format:
- Underlying ticker
- Expiration date (YYMMDD)
- Option type (C for Call, P for Put)
- Strike price (padded with leading zeros)

**Example Usage**:
```python
# Query SPY Call option, expiring July 7, 2025, with $450 strike price
params = {
    "full_symbol": "OPTION:US:SPY250707C00450000",
    # Additional parameters
}
```

## Using Asset Types in API Calls

When making API calls, you can specify the asset type as part of the `full_symbol` parameter or use it with the SchemaAsset enum:

```python
from aitrados_api import SchemaAsset

# Using SchemaAsset enum
params = {
    "schema_asset": SchemaAsset.CRYPTO,
    "country_symbol": "GLOBAL:BTCUSDT",
    # Additional parameters
}
```