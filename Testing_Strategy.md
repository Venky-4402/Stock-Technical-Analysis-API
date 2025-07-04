# Testing Strategy

This brief outlines the testing approach used for the Kalpi Technical Indicator API, ensuring correctness, security, and compliance with tiered subscription requirements.

## 1. Automated Unit and Integration Tests

- **Unit tests** cover core logic for indicator calculations (SMA, EMA, RSI, MACD, Bollinger Bands) using sample data to verify mathematical correctness.
- **Integration tests** use FastAPI’s TestClient to simulate real HTTP requests, validating end-to-end API behavior including authentication, authorization, and response formatting.

## 2. Tier and Rate Limiting Validation

- **Tier-based access tests** confirm that Free, Pro, and Premium users can only access endpoints and data ranges allowed by their subscription.
- **Rate limiting tests** simulate exceeding daily request quotas and verify correct 429 (Too Many Requests) responses.
- **Forbidden access tests** ensure that attempts to access restricted indicators or data ranges return 403 errors.

## 3. Security and Error Handling

- **Authentication tests** check that endpoints require valid JWT tokens and reject invalid or expired tokens with 401 responses.
- **Input validation tests** submit malformed or incomplete requests to ensure the API returns appropriate 422 errors.
- **Edge case tests** include invalid dates, unknown symbols, and boundary conditions for indicator parameters.

## 4. Caching and Performance

- **Cache hit/miss tests** verify that repeated requests for the same indicator and parameters are served from cache, improving response times.
- **Performance checks** ensure the API responds efficiently under typical and peak loads.

## 5. Manual and Exploratory Testing

- Used Swagger UI to manually test endpoints, try different scenarios, and visually inspect request/response examples.
- Verified API documentation accuracy and usability.

## 6. Continuous Testing

- All tests are run automatically with each code change to ensure ongoing correctness and prevent regressions.

---

This comprehensive approach ensures the API is robust, secure, and behaves correctly for all user tiers and scenarios.
