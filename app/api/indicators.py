from fastapi import APIRouter, Depends, HTTPException, status
from app.models.indicators import (
    IndicatorRequest, IndicatorResponse, MACDResponse, BollingerBandsResponse
)
from app.services import indicators
from app.auth.auth import get_current_user
from app.db.models import User
from app.cache.cache import cache_indicator, get_cached_indicator
import pandas as pd
import os
from datetime import datetime
from app.db.session import get_db
import math

def clean_nan(values):
    # Converts NaN and inf to None for JSON serialization
    return pd.Series(values).where(pd.notnull(values), None).tolist()


router = APIRouter(prefix="/indicators", tags=["Indicators"])

DATA_PATH = os.getenv("DATA_PATH", "stocks_ohlc_data.parquet")

# Helper function to enforce tier-based restrictions
def check_access(user: User, indicator: str, start_date: str, end_date: str):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    days_requested = (end - start).days

    if user.tier == "free":
        if indicator not in ["sma", "ema"]:
            raise HTTPException(status_code=403, detail="Free tier: Only SMA and EMA allowed.")
        if days_requested > 93:
            raise HTTPException(status_code=403, detail="Free tier: Max 3 months of data allowed.")
        if user.requests_today >= 50:
            raise HTTPException(status_code=429, detail="Free tier: Max 50 requests per day reached.")
    elif user.tier == "pro":
        if indicator not in ["sma", "ema", "rsi", "macd"]:
            raise HTTPException(status_code=403, detail="Pro tier: Only SMA, EMA, RSI, MACD allowed.")
        if days_requested > 366:
            raise HTTPException(status_code=403, detail="Pro tier: Max 1 year of data allowed.")
        if user.requests_today >= 500:
            raise HTTPException(status_code=429, detail="Pro tier: Max 500 requests per day reached.")
    elif user.tier == "premium":
        if indicator not in ["sma", "ema", "rsi", "macd", "bollinger", "vwap"]:
            raise HTTPException(status_code=403, detail="Premium tier: Indicator not supported.")
    else:
        raise HTTPException(status_code=403, detail="Unknown subscription tier.")

def increment_request_count(user: User, db_session):
    # You should implement logic to reset requests_today at midnight
    user.requests_today += 1
    db_session.commit()

def load_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    df = df[df['symbol'] == symbol]
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df = df.sort_values("date")
    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for given symbol and date range")
    return df

@router.post("/sma", response_model=IndicatorResponse)
def get_sma(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)  # Replace with your DB session dependency
):
    check_access(user, "sma", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:sma:{req.window}"
    cached = get_cached_indicator(key)
    if cached:
        return IndicatorResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    sma_values = indicators.sma(df, req.window)
    print("DEBUG values:", clean_nan(sma_values.tolist()))
    result = IndicatorResponse(
        dates=[str(d) for d in df['date'].tolist()],
        values=clean_nan(sma_values.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result

@router.post("/ema", response_model=IndicatorResponse)
def get_ema(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)
):
    check_access(user, "ema", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:ema:{req.window}"
    cached = get_cached_indicator(key)
    if cached:
        return IndicatorResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    ema_values = indicators.ema(df, req.window)
    result = IndicatorResponse(
        dates=[str(d) for d in df['date'].tolist()],
        values=clean_nan(ema_values.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result

@router.post("/rsi", response_model=IndicatorResponse)
def get_rsi(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)
):
    check_access(user, "rsi", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:rsi:{req.period}"
    cached = get_cached_indicator(key)
    if cached:
        return IndicatorResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    rsi_values = indicators.compute_rsi(df["close"], req.period)
    result = IndicatorResponse(
        dates=[str(d) for d in df['date'].tolist()],
        values=clean_nan(rsi_values.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result

@router.post("/macd", response_model=MACDResponse)
def get_macd(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)
):
    check_access(user, "macd", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:macd:{req.slow}:{req.fast}:{req.signal_period}"
    cached = get_cached_indicator(key)
    if cached:
        return MACDResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    macd_line, signal_line = indicators.macd(df, req.slow, req.fast, req.signal_period)
    result = MACDResponse(
        dates=[str(d) for d in df['date'].tolist()],
        macd=clean_nan(macd_line.tolist()),
        signal=clean_nan(signal_line.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result

@router.post("/bollinger", response_model=BollingerBandsResponse)
def get_bollinger(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)
):
    check_access(user, "bollinger", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:bollinger:{req.window}:{req.std_multiplier}"
    cached = get_cached_indicator(key)
    if cached:
        return BollingerBandsResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    upper, lower = indicators.bollinger_bands(df, req.window, req.std_multiplier)
    result = BollingerBandsResponse(
        dates=[str(d) for d in df['date'].tolist()],
        upper_band=clean_nan(upper.tolist()),
        lower_band=clean_nan(lower.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result

@router.post("/vwap", response_model=IndicatorResponse)
def get_vwap(
    req: IndicatorRequest,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db)
):
    check_access(user, "vwap", req.start_date, req.end_date)
    key = f"{req.symbol}:{req.start_date}:{req.end_date}:vwap"
    cached = get_cached_indicator(key)
    if cached:
        return IndicatorResponse(**cached)
    df = load_data(req.symbol, req.start_date, req.end_date)
    vwap_values = indicators.vwap(df)
    result = IndicatorResponse(
        dates=[str(d) for d in df['date'].tolist()],
        values=clean_nan(vwap_values.tolist())
    )
    cache_indicator(key, result.dict())
    increment_request_count(user, db_session)
    return result
