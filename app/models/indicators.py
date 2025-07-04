# Import BaseModel from Pydantic for data validation
from pydantic import BaseModel
 # Import List for type hinting lists
from typing import List
# Defines the request structure for technical indicator calculations
class IndicatorRequest(BaseModel):
    
    symbol: str# Stock symbol
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD
    window: int = 14 # Window period for SMA/EMA
    period: int = 14 # Period for RSI
    slow: int = 26 # Slow period for MACD
    fast: int = 12 # Fast period for MACD
    signal_period: int = 9 # Signal period for MACD
    std_multiplier: float = 2.0 # Standard deviation multiplier for Bollinger Bands

class IndicatorResponse(BaseModel):
    dates: List[str] # List of dates in string format
    values: List[float] # List of calculated indicator values

class MACDResponse(BaseModel):
    dates: List[str]
    macd: List[float] # List of MACD line values
    signal: List[float] # List of Signal line values

class BollingerBandsResponse(BaseModel):
    dates: List[str]
    upper_band: List[float] # List of upper Bollinger Band values
    lower_band: List[float] # List of lower Bollinger Band values
