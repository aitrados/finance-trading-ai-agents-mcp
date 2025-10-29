
from typing import List
import polars as pl


class TraditionalIndicatorOps:
    valid_indicators = {"MA", "MACD", "BOLL", "RSI", "EMA"}
    def __init__(self, ohlc_data: dict, indicators: List[str], ma_periods: List[int] = None):
        self.ohlc_data = ohlc_data
        self.indicators = [ind.upper() for ind in indicators]  # Convert to uppercase
        self.ma_periods = ma_periods or [5,10, 20, 60]
        self.added_columns = []  # Record added column names
        self.__init()
    def __init(self):

        invalid_indicators = set(self.indicators) - self.valid_indicators
        if invalid_indicators:
            raise ValueError(f"Unsupported indicators: {invalid_indicators}.Only support {self.valid_indicators}")

    def _calculate_ema(self, df: pl.DataFrame, periods: List[int] = None) -> pl.DataFrame:
        """Calculate Exponential Moving Average"""
        if periods is None:
            periods = self.ma_periods or [12, 26]  # use macd args

        for period in periods:
            col_name = f"ema_{period}"
            df = df.with_columns(
                pl.col("close").ewm_mean(span=period).alias(col_name)
            )
            self.added_columns.append(col_name)
        return df


    def _calculate_ma(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate Moving Average"""
        if not self.ma_periods:
            raise ValueError("MA indicator requires ma_periods parameter")

        for period in self.ma_periods:
            col_name = f"ma_{period}"
            df = df.with_columns(
                pl.col("close").rolling_mean(window_size=period).alias(col_name)
            )
            self.added_columns.append(col_name)
        return df

    def _calculate_rsi(self, df: pl.DataFrame, period: int = 14) -> pl.DataFrame:
        """Calculate RSI indicator"""
        df = df.with_columns(
            (pl.col("close") - pl.col("close").shift(1)).alias("price_change")
        )

        df = df.with_columns([
            pl.when(pl.col("price_change") > 0).then(pl.col("price_change")).otherwise(0).alias("gain"),
            pl.when(pl.col("price_change") < 0).then(-pl.col("price_change")).otherwise(0).alias("loss")
        ])

        df = df.with_columns([
            pl.col("gain").rolling_mean(window_size=period).alias("avg_gain"),
            pl.col("loss").rolling_mean(window_size=period).alias("avg_loss")
        ])

        df = df.with_columns(
            (pl.col("avg_gain") / pl.col("avg_loss")).alias("rs")
        )

        df = df.with_columns(
            (100 - (100 / (1 + pl.col("rs")))).alias("rsi")
        )

        df = df.drop(["price_change", "gain", "loss", "avg_gain", "avg_loss", "rs"])
        self.added_columns.append("rsi")
        return df

    def _calculate_macd(self, df: pl.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pl.DataFrame:
        """Calculate MACD indicator"""
        df = df.with_columns([
            pl.col("close").ewm_mean(span=fast).alias(f"ema_{fast}"),
            pl.col("close").ewm_mean(span=slow).alias(f"ema_{slow}")
        ])

        df = df.with_columns(
            (pl.col(f"ema_{fast}") - pl.col(f"ema_{slow}")).alias("macd_dif")
        )

        df = df.with_columns(
            pl.col("macd_dif").ewm_mean(span=signal).alias("macd_dea")
        )

        df = df.with_columns(
            (pl.col("macd_dif") - pl.col("macd_dea")).alias("macd_histogram")
        )

        df = df.drop([f"ema_{fast}", f"ema_{slow}"])
        self.added_columns.extend(["macd_dif", "macd_dea", "macd_histogram"])
        return df

    def _calculate_boll(self, df: pl.DataFrame, period: int = 20, std_dev: float = 2.0) -> pl.DataFrame:
        """Calculate Bollinger Bands indicator"""
        df = df.with_columns(
            pl.col("close").rolling_mean(window_size=period).alias("boll_mid")
        )

        df = df.with_columns(
            pl.col("close").rolling_std(window_size=period).alias("boll_std")
        )

        df = df.with_columns([
            (pl.col("boll_mid") + std_dev * pl.col("boll_std")).alias("boll_upper"),
            (pl.col("boll_mid") - std_dev * pl.col("boll_std")).alias("boll_lower")
        ])

        df = df.drop(["boll_std"])
        self.added_columns.extend(["boll_upper", "boll_mid", "boll_lower"])
        return df



    def _calculate_df(self, df: pl.DataFrame):

        if "MA" in self.indicators:
            df = self._calculate_ma(df)

        if "RSI" in self.indicators:
            df = self._calculate_rsi(df)

        if "MACD" in self.indicators:
            df = self._calculate_macd(df)

        if "BOLL" in self.indicators:
            df = self._calculate_boll(df)
        if "EMA" in self.indicators:
            df = self._calculate_ema(df)
        return df

    def get_result(self):
        for full_symbol in list(self.ohlc_data.keys()):
            for i, df in enumerate(self.ohlc_data[full_symbol]):

                modified_df = self._calculate_df(df)  # Calculate indicators, return new DataFrame
                # Reassign to the original data structure
                self.ohlc_data[full_symbol][i] = modified_df
        return self.ohlc_data, self.added_columns