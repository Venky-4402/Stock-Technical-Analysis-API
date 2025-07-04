# Setup and Running Instructions
## Kalpi Technical Indicator API

This document provides clear instructions for setting up and running the Kalpi Technical Indicator API locally, including how to test different subscription tiers.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Standard Setup (Without Docker)](#standard-setup-without-docker)
3. [Docker Setup](#docker-setup)
4. [Testing Different Subscription Tiers](#testing-different-subscription-tiers)
5. [API Endpoints](#api-endpoints)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Standard Setup Requirements
- Python 3.9+
- PostgreSQL 13+
- Redis (optional, for caching)
- Git

### Docker Setup Requirements
- Docker
- Docker Compose

## Standard Setup (Without Docker)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/kalpi-technical-indicators.git
cd kalpi-technical-indicators
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL
```bash
# Create database
createdb kalpi_indicators

# Set environment variables
# On Windows
set DATABASE_URL=postgresql://username:password@localhost/kalpi_indicators
# On macOS/Linux
export DATABASE_URL=postgresql://username:password@localhost/kalpi_indicators
```

### 5. Initialize Database
```bash
python scripts/init_db.py
```

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

### 7. Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/kalpi-technical-indicators.git
cd kalpi-technical-indicators
```

### 2. Build and Start Docker Containers
```bash
docker-compose up -d
```

This will:
- Start a PostgreSQL container
- Start a Redis container (for caching)
- Build and start the API container
- Set up all necessary networking

The API will be available at: http://localhost:8000

### 3. Initialize Database (First Run Only)
```bash
docker-compose exec api python scripts/init_db.py
```

### 4. Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing Different Subscription Tiers

The API includes a test script to create users with different subscription tiers.

### 1. Run the Test Users Script
```bash
# Without Docker
python scripts/create_test_users.py

# With Docker
docker-compose exec api python scripts/create_test_users.py
```

### 2. Test User Credentials

| Username | Password | Tier     |
|----------|----------|----------|
| free     | pass123  | Free     |
| pro      | pass123  | Pro      |
| premium  | pass123  | Premium  |

### 3. Testing with cURL

#### Get Authentication Token
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -d "username=free&password=pass123" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Test an Endpoint
```bash
curl -X POST "http://localhost:8000/indicators/sma" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RELIANCE",
    "start_date": "2023-01-01",
    "end_date": "2023-03-31",
    "window": 14
  }'
```

### 4. Testing Tier Restrictions

#### Free Tier Limitations
- Try accessing RSI (should return 403 Forbidden)
- Try accessing data older than 3 months (should return 403 Forbidden)
- Make 51+ requests in a day (should return 429 Too Many Requests)

#### Pro Tier Limitations
- Try accessing Bollinger Bands (should return 403 Forbidden)
- Try accessing data older than 1 year (should return 403 Forbidden)
- Make 501+ requests in a day (should return 429 Too Many Requests)

#### Premium Tier
- Should have access to all indicators
- Should have access to full 3 years of data
- Should have unlimited requests

## API Endpoints

| Endpoint                | Method | Description                    | Available Tiers        |
|-------------------------|--------|--------------------------------|------------------------|
| /auth/register          | POST   | Register a new user            | All                    |
| /auth/token             | POST   | Get JWT token                  | All                    |
| /indicators/sma         | POST   | Simple Moving Average          | Free, Pro, Premium     |
| /indicators/ema         | POST   | Exponential Moving Average     | Free, Pro, Premium     |
| /indicators/rsi         | POST   | Relative Strength Index        | Pro, Premium           |
| /indicators/macd        | POST   | MACD                           | Pro, Premium           |
| /indicators/bollinger   | POST   | Bollinger Bands                | Premium                |

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials
- Ensure database exists

```bash
# Test database connection
python -c "from app.db.session import get_db; next(get_db()); print('Connection successful')"
```

### API Not Starting
- Check for port conflicts
- Verify Python version (3.9+)
- Check logs for detailed errors

### Docker Issues
- Verify Docker is running
- Check container status
```bash
docker-compose ps
```
- View logs
```bash
docker-compose logs -f api
```

### Rate Limiting Issues
- The rate limit counter resets at midnight UTC
- To reset for testing:
```bash
# Without Docker
python scripts/reset_rate_limits.py

# With Docker
docker-compose exec api python scripts/reset_rate_limits.py
```

## Additional Information

- The application uses JWT tokens with a 30-minute expiration
- Rate limits are tracked per user in the database
- Cached results expire after 24 hours
- All dates should be in YYYY-MM-DD format
