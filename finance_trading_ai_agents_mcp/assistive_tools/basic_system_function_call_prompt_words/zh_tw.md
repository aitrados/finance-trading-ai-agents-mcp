# 當你在呼叫 function calls 時，涉及到函數變數請參考如下格式：

## 1. `full_symbol` 參數：
這是一個結構化的字串，格式為 `ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL`。

*   **ASSET_NAME**：金融工具的類別。
    *   有效值只支援：`STOCK`, `FOREX`, `CRYPTO`, `FUTURE`, `OPTION`。
*   **COUNTRY_ISO_CODE**：市場或國家代碼。
    *   有效值範例：`US`（美國）、`CN`（中國大陸）、`HK`（香港）、`JP`（日本）、`UK`（英國）、`AU`（澳洲）、`GLOBAL`（全球）等。
    *   `GLOBAL` 是一個特殊的 COUNTRY_ISO_CODE，目前只有 `FOREX`、`CRYPTO` 使用 `GLOBAL`。
*   **SYMBOL**：具體的交易代碼/代號。

**【重要範例】**
*   若使用者只提供 SYMBOL 或公司名稱，而你已經知道其對應的 ASSET_NAME 與 COUNTRY_ISO_CODE，請自動補齊。例如使用者問：「近期蘋果股票怎麼樣？」 -> `full_symbol` 為 `STOCK:US:AAPL`。
*   「近期特斯拉股票怎麼樣？」 -> `full_symbol` 必須為：`STOCK:US:TSLA`。
*   「歐元兌美元的匯率」 -> `full_symbol` 必須為：`FOREX:GLOBAL:EURUSD`。
*   「查一下騰訊在香港的股價」 -> `full_symbol` 必須為：`STOCK:HK:00700`。
*   「比特幣價格」 -> `full_symbol` 必須為：`CRYPTO:GLOBAL:BTCUSD`。
*   「中國平安的股票」 -> `full_symbol` 必須為：`STOCK:CN:601318`。

**【符號自動推斷規則】**
*   優先根據使用者的語言與上下文推斷市場，如中文公司名預設推斷為中國市場。
*   若為知名美國公司，預設使用美股市場（US）。
*   加密貨幣與外匯一律使用 GLOBAL。
*   如有歧義時，選擇最主要的交易市場。

## 2. `interval` 參數：
此參數定義 OHLC 數據的時間週期。

*   你必須從下列清單中選擇一個最符合使用者需求的值：
    `MON`（月線）、`WEEK`（週線）、`DAY`（日線）、`240M`（4 小時）、`120M`（2 小時）、`60M`（1 小時）、`30M`（30 分鐘）、`15M`（15 分鐘）、`10M`（10 分鐘）、`5M`（5 分鐘）、`3M`（3 分鐘）、`1M`（1 分鐘）。
*   若使用者的描述較模糊（如「小時線」），請選擇最常用的 `60M`。
*   若使用者未明確指定時間週期，預設使用 `DAY`。
*   時間週期選擇建議：
    *   長期分析：`MON` 或 `WEEK`
    *   日常分析：`DAY`
    *   短線交易：`60M`, `30M`, `15M`
    *   超短線交易：`5M`, `3M`, `1M`

## 3. `format` 參數:
*   目前支援: `json`, `csv`
*   **預設使用 `csv`** \- 減少字串長度，提升傳輸效率。除非使用者明確要求，否則必須使用 `csv`
*   `json` 格式較適合複雜結構化資料
*   若未指定，必須選擇 `csv`

## 4. `limit` 參數:
*   限制輸出列數 \- 列數越多 = 字串越長
*   除非使用者明確指定 `limit`，否則必須使用預設值

# OHLC 資料工具選擇（必須優先實時串流資料呼叫）
## 1. 在呼叫 OHLC 函數時，若無特殊需求，必須優先名稱包含 `live_streaming_ohlc` 的函數
## 2. 對於多時框交易需求（需要時間視窗對齊），使用名稱包含 `multi_timeframe_live_streaming_ohlc` 的函數
## 3. 對於多標的多時框混合交易（需要時間框對齊），使用名稱包含 `multi_symbol_multi_timeframe_live_streaming_ohlc` 的函數
