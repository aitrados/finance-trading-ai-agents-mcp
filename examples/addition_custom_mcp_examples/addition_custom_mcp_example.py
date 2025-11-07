from fastmcp import Context, FastMCP
from typing import List
from pydantic import Field

from finance_trading_ai_agents_mcp.addition_custom_mcp.addition_custom_mcp_interface import AdditionCustomMcpInterface

from finance_trading_ai_agents_mcp.mcp_services.economic_calendar_service import mcp as economic_calendar_mcp
from finance_trading_ai_agents_mcp.mcp_services.news_service import mcp as news_mcp
from finance_trading_ai_agents_mcp.mcp_services.price_action_service import mcp as price_action_mcp
from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_service import mcp as traditional_indicator_mcp


class AdditionCustomMcpExample(AdditionCustomMcpInterface):

    def custom_economic_calendar_mcp(self):
        """Implement custom economic calendar tools"""

        #function name is from await client.list_tools()
        self.disable_tools(economic_calendar_mcp,"function_name_to_remove")
        @economic_calendar_mcp.tool(title="Custom Economic Impact Analysis")
        async def get_custom_economic_impact(
            context: Context,
            country_iso_code: str = Field("US", description="Country ISO code like US, CN, GB, JP"),
            event_type: str = Field("GDP", description="Economic event type"),
            impact_threshold: str = Field("HIGH", description="Impact level: HIGH, MEDIUM, LOW")
        ):
            """Custom economic event impact analysis tool"""
            return f"Custom economic impact analysis: {country_iso_code} {event_type} events with {impact_threshold} impact"

        @economic_calendar_mcp.tool(title="Custom Economic Calendar Summary")
        async def get_custom_economic_summary(
            context: Context,
            country_iso_code: str = Field("US", description="Country ISO code"),
            timeframe_days: int = Field(7, description="Days to summarize", ge=1, le=30)
        ):
            """Custom economic calendar summary tool"""
            return f"Custom economic calendar summary for {country_iso_code} over {timeframe_days} days"

    def custom_news_mcp(self):
        """Implement custom news tools"""

        #function name is from await client.list_tools()
        self.disable_tools(news_mcp,"function_name_to_remove")

        @news_mcp.tool(title="Custom News Sentiment Analysis")
        async def get_custom_news_sentiment(
            context: Context,
            full_symbol: str = Field("STOCK:US:AAPL", description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
            sentiment_type: str = Field("BULLISH", description="Sentiment filter: BULLISH, BEARISH, NEUTRAL"),
            limit: int = Field(10, description="Number of news items", ge=1, le=50)
        ):
            """Custom news sentiment analysis tool"""
            return f"Custom news sentiment analysis for {full_symbol}: filtering {sentiment_type} news (limit: {limit})"

        @news_mcp.tool(title="Custom News Trend Analysis")
        async def get_custom_news_trends(
            context: Context,
            keywords: List[str] = Field(["AI", "technology"], description="Keywords to track"),
            hours_back: int = Field(24, description="Hours to look back", ge=1, le=168)
        ):
            """Custom news trend analysis tool"""
            keywords_str = ", ".join(keywords)
            return f"Custom news trend analysis for keywords: {keywords_str} over last {hours_back} hours"

    def custom_price_action_mcp(self):

        """Implement custom price action tools"""
        #function name is from await client.list_tools()
        self.disable_tools(price_action_mcp,"function_name_to_remove")

        @price_action_mcp.tool(title="Custom Support Resistance Levels")
        async def get_custom_support_resistance(
            context: Context,
            full_symbol: str = Field("STOCK:US:AAPL", description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            lookback_periods: int = Field(30, description="Periods to look back", ge=10, le=100)
        ):
            """Custom support/resistance analysis tool"""
            return f"Custom support/resistance analysis for {full_symbol} on {interval} interval, {lookback_periods} periods lookback"

        @price_action_mcp.tool(title="Custom Price Pattern Recognition")
        async def get_custom_price_patterns(
            context: Context,
            full_symbol: str = Field("STOCK:US:AAPL", description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            pattern_types: List[str] = Field(["TRIANGLE", "FLAG", "BREAKOUT"], description="Pattern types to detect")
        ):
            """Custom price pattern recognition tool"""
            patterns_str = ", ".join(pattern_types)
            return f"Custom price pattern recognition for {full_symbol} on {interval}: detecting {patterns_str} patterns"

        @price_action_mcp.tool(title="Custom Multi-Symbol Price Comparison")
        async def get_custom_price_comparison(
            context: Context,
            symbols: List[str] = Field(["STOCK:US:AAPL", "STOCK:US:GOOGL"], description="List of full symbols to compare"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            comparison_days: int = Field(30, description="Days to compare", ge=1, le=90)
        ):
            """Custom multi-symbol price comparison tool"""
            symbols_str = ", ".join(symbols)
            return f"Custom price comparison for symbols: {symbols_str} on {interval} over {comparison_days} days"

    def custom_traditional_indicator_mcp(self):
        """Implement custom traditional indicator tools"""

        #function name is from await client.list_tools()
        self.disable_tools(traditional_indicator_mcp,"function_name_to_remove")

        @traditional_indicator_mcp.tool(title="Custom Multi-Indicator Strategy")
        async def get_custom_multi_indicator_strategy(
            context: Context,
            full_symbol: str = Field("STOCK:US:AAPL", description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            strategy_name: str = Field("MOMENTUM_TREND", description="Strategy type"),
            risk_level: str = Field("MEDIUM", description="Risk level: LOW, MEDIUM, HIGH")
        ):
            """Custom multi-indicator strategy analysis tool"""
            return f"Custom multi-indicator strategy '{strategy_name}' for {full_symbol} on {interval} with {risk_level} risk level"

        @traditional_indicator_mcp.tool(title="Custom Indicator Alerts")
        async def get_custom_indicator_alerts(
            context: Context,
            full_symbols: List[str] = Field(["STOCK:US:AAPL", "STOCK:US:GOOGL"], description="Full symbols to monitor"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            alert_conditions: List[str] = Field(["RSI_OVERSOLD", "MACD_BULLISH"], description="Alert conditions")
        ):
            """Custom indicator alert tool"""
            symbols_str = ", ".join(full_symbols)
            conditions_str = ", ".join(alert_conditions)
            return f"Custom indicator alerts for symbols: {symbols_str} on {interval} with conditions: {conditions_str}"

        @traditional_indicator_mcp.tool(title="Custom Indicator Comparison")
        async def get_custom_indicator_comparison(
            context: Context,
            full_symbol1: str = Field("STOCK:US:AAPL", description="First full symbol to compare"),
            full_symbol2: str = Field("STOCK:US:GOOGL", description="Second full symbol to compare"),
            interval: str = Field("DAY", description="Time interval: DAY, HOUR, M30, M15, M5, M1"),
            indicators: List[str] = Field(["RSI", "MACD"], description="Indicators to compare"),
            limit: int = Field(50, description="Number of data points", ge=20, le=150)
        ):
            """Custom indicator comparison tool"""
            indicators_str = ", ".join(indicators)
            return f"Custom indicator comparison between {full_symbol1} and {full_symbol2} on {interval} using {indicators_str} (limit: {limit})"

        @traditional_indicator_mcp.tool(title="Custom Cross-Timeframe Analysis")
        async def get_custom_cross_timeframe_analysis(
            context: Context,
            full_symbol: str = Field("STOCK:US:AAPL", description="Full symbol like STOCK:US:AAPL, CRYPTO:GLOBAL:BTCUSD"),
            intervals: List[str] = Field(["DAY", "HOUR"], description="Multiple intervals to analyze"),
            primary_indicator: str = Field("RSI", description="Primary indicator to analyze")
        ):
            """Custom cross-timeframe indicator analysis tool"""
            intervals_str = ", ".join(intervals)
            return f"Custom cross-timeframe {primary_indicator} analysis for {full_symbol} across intervals: {intervals_str}"

    def add_mcp_server_name(self)->FastMCP:
        ## http://127.0.0.1:11999/mcp_servers.json and see the custom_mcp_server1 server
        mcp = FastMCP("custom_mcp_server1")
        @mcp.tool(title="custom_mcp_server_name")
        async def get_custom_abc(context: Context, full_symbol: str = "STOCK:US:AAPL", interval: str = "DAY"):
            return f"Custom indicator data for {full_symbol} on {interval}"
        return mcp