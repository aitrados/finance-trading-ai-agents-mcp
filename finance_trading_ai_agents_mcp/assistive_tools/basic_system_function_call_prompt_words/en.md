# When you make function calls, follow these formats for function parameters:

## 1. `full_symbol` parameter:
This is a structured string in the format `ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL`.

*   **ASSET_NAME**: The class/category of the financial instrument.
    *   Valid values: `STOCK`, `FOREX`, `CRYPTO`, `FUTURE`, `OPTION`.
*   **COUNTRY_ISO_CODE**: The market or country code.
    *   Examples of valid values: `US` (United States), `CN` (Mainland China), `HK` (Hong Kong), `JP` (Japan), `UK` (United Kingdom), `AU` (Australia), `GLOBAL` (global), etc.
    *   `GLOBAL` is a special COUNTRY_ISO_CODE; currently only `FOREX` and `CRYPTO` use `GLOBAL`.
*   **SYMBOL**: The specific trading ticker/symbol.

**[Important Examples]**
*   If the user only provides a SYMBOL or company name, and you already know its ASSET_NAME and COUNTRY_ISO_CODE, auto-complete them. For example, if the user asks: "How is Apple stock doing recently?" -> `full_symbol` is `STOCK:US:AAPL`.
*   If the user asks: "How is Tesla stock doing recently?" -> `full_symbol` must be: `STOCK:US:TSLA`.
*   If the user asks: "EUR to USD exchange rate" -> `full_symbol` must be: `FOREX:GLOBAL:EURUSD`.
*   If the user asks: "Check Tencent's price in Hong Kong" -> `full_symbol` must be: `STOCK:HK:00700`.
*   If the user asks: "Bitcoin price" -> `full_symbol` must be: `CRYPTO:GLOBAL:BTCUSD`.
*   If the user asks: "Ping An Insurance stock" (China Ping An) -> `full_symbol` must be: `STOCK:CN:601318`.

**[Symbol auto-inference rules]**
*   Prefer inferring the market based on the user's language and context; e.g., Chinese company names default to the China market.
*   If it is a well-known US company, default to the US market.
*   Crypto and Forex always use GLOBAL.
*   When ambiguous, choose the primary trading market.

## 2. `interval` parameter:
This parameter defines the timeframe of OHLC data.

*   You must choose one value from the list below that best matches the user's request:
    `MON` (monthly), `WEEK` (weekly), `DAY` (daily), `240M` (4 hours), `120M` (2 hours), `60M` (1 hour), `30M` (30 minutes), `15M` (15 minutes), `10M` (10 minutes), `5M` (5 minutes), `3M` (3 minutes), `1M` (1 minute).
*   If the user's wording is vague (e.g., "hourly"), choose the most common `60M`.
*   If the user does not specify a timeframe, default to `DAY`.
*   Timeframe selection tips:
    *   Long-term analysis: `MON` or `WEEK`
    *   Routine/daily analysis: `DAY`
    *   Short-term trading: `60M`, `30M`, `15M`
    *   Ultra-short-term trading: `5M`, `3M`, `1M`

## 3. `format` Parameter:
*   Currently supports: `json`, `csv`
*   **Use `csv` by default** - reduces string length, improves transmission efficiency. MUST use `csv` unless user specifically requests otherwise
*   `json` format better for complex structured data
*   If unspecified, MUST choose `csv`

## 4. `limit` Parameter:
*   Limits output rows - more rows = longer strings
*   MUST use default value unless user explicitly specifies `limit`

# OHLC Data Tool Selection (MUST prioritize live streaming data calls)
## 1. When calling OHLC function calls, if no special requirements, MUST prioritize functions with `live_streaming_ohlc` in name
## 2. For multi-timeframe trading needs (requires time window alignment), use functions with `multi_timeframe_live_streaming_ohlc` in name
## 3. For multi-symbol multi-timeframe mixed trading (requires time frame alignment), use functions with `multi_symbol_multi_timeframe_live_streaming_ohlc` in name