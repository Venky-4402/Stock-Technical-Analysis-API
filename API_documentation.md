# Kalpi Technical Indicator API Documentation

## Overview

This API provides technical indicators for stock data based on OHLC (Open, High, Low, Close) daily prices.  
It supports multiple subscription tiers with different access levels and rate limits.

## Base URL

```
http://localhost:8000/
```

## Authentication

- **Method:** JWT Bearer Token
- **Login Endpoint:** `/auth/token`
- **Register Endpoint:** `/auth/register`

## Endpoints

### 1. User Registration

**POST** `/auth/register`

Register a new user.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**

- `200 OK` on success
- `400 Bad Request` if username already exists

### 2. User Login / Token Generation

**POST** `/auth/token`

Get JWT access token.

**Request Form Data:**

- `username`: string
- `password`: string

**Response:**

```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer"
}
```

### 3. Simple Moving Average (SMA)

**POST** `/indicators/sma`

Calculate SMA for a stock symbol over a date range.

**Request Body:**

```json
{
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2023-03-31",
  "window": 14
}
```

**Response:**

```json
{
  "dates": ["2023-01-01", "2023-01-02", "..."],
  "values": [123.45, 124.56, "..."]
}
```

**Access:** Free, Pro, Premium tiers  
**Rate Limit:** Free (50/day), Pro (500/day), Premium (Unlimited)  
**Data Range:** Free (last 3 months), Pro (last 1 year), Premium (full 3 years)

### 4. Exponential Moving Average (EMA)

**POST** `/indicators/ema`

Calculate EMA for a stock symbol over a date range.

**Request Body:**

```json
{
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2023-03-31",
  "window": 14
}
```

**Response:**

```json
{
  "dates": ["2023-01-01", "2023-01-02", "..."],
  "values": [123.45, 124.56, "..."]
}
```

**Access:** Free, Pro, Premium tiers  
**Rate Limit:** Same as SMA  
**Data Range:** Same as SMA

### 5. Relative Strength Index (RSI)

**POST** `/indicators/rsi`

Calculate RSI for a stock symbol over a date range.

**Request Body:**

```json
{
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2023-03-31",
  "period": 14
}
```

**Response:**

```json
{
  "dates": ["2023-01-01", "2023-01-02", "..."],
  "values": [55.3, 57.1, "..."]
}
```

**Access:** Pro, Premium tiers only  
**Rate Limit:** Pro (500/day), Premium (Unlimited)  
**Data Range:** Pro (last 1 year), Premium (full 3 years)

### 6. Moving Average Convergence Divergence (MACD)

**POST** `/indicators/macd`

Calculate MACD for a stock symbol over a date range.

**Request Body:**

```json
{
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2023-03-31",
  "fast": 12,
  "slow": 26,
  "signal_period": 9
}
```

**Response:**

```json
{
  "dates": ["2023-01-01", "2023-01-02", "..."],
  "macd": [0.5, 0.6, "..."],
  "signal": [0.4, 0.5, "..."]
}
```

**Access:** Pro, Premium tiers only  
**Rate Limit:** Pro (500/day), Premium (Unlimited)  
**Data Range:** Pro (last 1 year), Premium (full 3 years)

### 7. Bollinger Bands

**POST** `/indicators/bollinger`

Calculate Bollinger Bands for a stock symbol over a date range.

**Request Body:**

```json
{
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2023-03-31",
  "period": 20,
  "std_multiplier": 2.0
}
```

**Response:**

```json
{
  "dates": ["2023-01-01", "2023-01-02", "..."],
  "upper_band": [130.5, 131.0, "..."],
  "lower_band": [120.5, 121.0, "..."]
}
```

**Access:** Premium tier only  
**Rate Limit:** Unlimited  
**Data Range:** Full 3 years

## Error Responses

| Status Code | Description                                         |
|-------------|-----------------------------------------------------|
| 400         | Bad request (invalid input or missing fields)       |
| 401         | Unauthorized (invalid or missing token)              |
| 403         | Forbidden (exceeded tier limits or unauthorized access) |
| 429         | Too Many Requests (rate limit exceeded)              |
| 422         | Validation error (invalid data format)                |
| 500         | Internal server error                                 |

## Authentication Example

**Register:**

```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"username":"user1","password":"pass1"}'
```

**Login:**

```bash
curl -X POST "http://localhost:8000/auth/token" -d "username=user1&password=pass1"
```

**Use Token:**

```bash
curl -X POST "http://localhost:8000/indicators/sma" -H "Authorization: Bearer " -H "Content-Type: application/json" -d '{"symbol":"RELIANCE","start_date":"2023-01-01","end_date":"2023-03-31","window":14}'
```

## Notes on Subscription Tiers

| Tier     | Request Limit (per day) | Allowed Indicators           | Allowed Data Range       |
|----------|-------------------------|-----------------------------|-------------------------|
| Free     | 50                      | SMA, EMA                    | Last 3 months           |
| Pro      | 500                     | SMA, EMA, RSI, MACD         | Last 1 year             |
| Premium  | Unlimited               | All indicators (incl. Bollinger Bands) | Full 3 years            |
