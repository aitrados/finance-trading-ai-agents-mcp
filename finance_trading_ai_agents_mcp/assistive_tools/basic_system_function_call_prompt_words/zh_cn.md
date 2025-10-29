# 当你在调用 function calls 时，涉及到函数变量请参考如下格式:

## 1. `full_symbol` 参数:
这是一个结构化的字符串，格式为 `ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL`。

*   **ASSET_NAME**: 金融工具的类别。
    *   有效值只支持: `STOCK`, `FOREX`, `CRYPTO`, `FUTURE`, `OPTION`。
*   **COUNTRY_ISO_CODE**: 市场或国家代码。
    *   有效值示例: `US` (美国), `CN` (中国大陆), `HK` (香港), `JP` (日本), `UK` (英国), `AU` (澳大利亚), `GLOBAL` (全球) 等。
    *   `GLOBAL`是一个特殊的COUNTRY_ISO_CODE，目前只有`FOREX`, `CRYPTO`使用`GLOBAL`。
*   **SYMBOL**: 具体的交易代码。

**【重要示例】**
*   如果用户只提供了SYMBOL 或者公司名字，如果你已经知道它属于的ASSET_NAME和COUNTRY_ISO_CODE，你自动补齐。比如用户问: "近期苹果股票怎么样?" -> `full_symbol` 是`STOCK:US:AAPL`
*   如果用户问: "近期特斯拉股票怎么样?" -> `full_symbol` 必须是: `STOCK:US:TSLA`
*   如果用户问: "欧元兑美元的汇率" -> `full_symbol` 必须是: `FOREX:GLOBAL:EURUSD`
*   如果用户问: "查一下腾讯在香港的股价" -> `full_symbol` 必须是: `STOCK:HK:00700`
*   如果用户问: "比特币价格" -> `full_symbol` 必须是: `CRYPTO:GLOBAL:BTCUSD`
*   如果用户问: "中国平安的股票" -> `full_symbol` 必须是: `STOCK:CN:601318`

**【符号自动推断规则】**
*   优先根据用户的语言和上下文推断市场，如中文公司名默认推断为中国市场
*   如果是知名的美国公司，默认使用US市场
*   加密货币和外汇始终使用GLOBAL
*   如有歧义时，选择最主要的交易市场

## 2. `interval` 参数:
这个参数定义了OHLC数据的时间周期。

*   **你必须**从以下列表中选择一个最符合用户请求的值:
    `MON` (月线), `WEEK` (周线), `DAY` (日线), `240M` (4小时), `120M` (2小时), `60M` (1小时), `30M` (30分钟), `15M` (15分钟), `10M` (10分钟), `5M` (5分钟), `3M` (3分钟), `1M` (1分钟)。
*   如果用户的表达比较模糊（如"小时线"），请选择最常用的 `60M`。
*   如果用户没有明确指定时间周期，默认使用 `DAY`。
*   **时间周期选择建议：**
    *   长期分析：`MON` 或 `WEEK`
    *   日常分析：`DAY`
    *   短线交易：`60M`, `30M`, `15M`
    *   超短线交易：`5M`, `3M`, `1M`

## 3. `format` 参数:
*   目前支持：`json`, `csv`
*   **推荐使用 `csv`**：可以有效减少字符串长度，提高传输效率,除非用户要求,否则必须使用`csv`
*   `json` 格式更适合复杂结构化数据处理
*   如用户未指定，必须选择 `csv`

## 4. `limit` 参数:
*   限制输出的行数，行数越大，字符串越长
*   除非用户明确了`limit`的长度,否则必须使用默认值

# OHLC 数据的工具选择(一定务必按照下面的方法优先调用实时流滚动数据)
## 1.当你调用蜡烛图数据(ohlc) function calls 时，如果用户没有做特别要求,一定要优先调用带有`live_streaming_ohlc`字符串的函数名
## 2.如果用户明确了多周期操盘需求,由于多周期需要时间窗口对齐,请使用带有`multi_timeframe_live_streaming_ohlc`字符串的函数名
## 3.如果户名明确了使用多周品多周期混合操盘,由于他们时间框架必须对齐,请使用带有`multi_symbol_multi_timeframe_live_streaming_ohlc`字符串的函数名