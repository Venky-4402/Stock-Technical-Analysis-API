import pandas as pd
#Computing RSI using close price and period over which RSI can be considered(most common and general being 14) using 100-100/(1+avg.gains/avg.losses)
def compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
#Computing Simple Moving Average for window period requested by taking rolling mean
def sma(data: pd.DataFrame, window_period: int) -> pd.Series:
    return data["close"].rolling(window=window_period).mean()
#Computing Exponential Moving Average for window period requested. ewm function helps us calculate ema.
def ema(data: pd.DataFrame, span: int) -> pd.Series:
    return data["close"].ewm(span=span, adjust=False).mean()
#Computing Moving Average Convergance Divergance which is short ema - long ema , through which we can calculate signal i.e, signal periad mean of macd.
def macd(data: pd.DataFrame, slow: int, fast: int, signal_period: int):
    macd_line = data["close"].ewm(span=fast, adjust=False).mean() - data["close"].ewm(span=slow, adjust=False).mean()
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, signal_line
#Computing Bollinger Bands technical Indicator to find lower and upper band of given stock.
def bollinger_bands(data: pd.DataFrame, period: int, std_multiplier: float):
    sma_ = data["close"].rolling(window=period).mean()
    std_ = data["close"].rolling(window=period).std()
    upper_band = sma_ + std_multiplier * std_
    lower_band = sma_ - std_multiplier * std_
    return upper_band, lower_band
#Calculating VWAP which is volume weighted average price
def vwap(data: pd.DataFrame) -> pd.Series:
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    tp_volume = typical_price * data['volume']
    cum_volume = data['volume'].cumsum()
    cum_tp_volume = tp_volume.cumsum()
    vwap = cum_tp_volume / cum_volume
    return vwap
