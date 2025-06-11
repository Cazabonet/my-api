import pytest
from fastapi import status
from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.core.rate_limit import rate_limiter


def test_logging_middleware(client, test_user):
    """Test logging middleware."""
    # Make a request
    response = client.get(f"/api/v1/pessoas/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Check if request was logged
    # Note: In a real test, we would check the log file
    # Here we just verify the middleware didn't break the request


def test_error_handling_middleware(client):
    """Test error handling middleware."""
    # Make a request to non-existent endpoint
    response = client.get("/api/v1/non-existent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Check if error was handled properly
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_rate_limit_middleware(client, test_user):
    """Test rate limit middleware."""
    # Make requests up to the limit
    for _ in range(60):  # Default rate limit is 60 requests per minute
        response = client.get(f"/api/v1/pessoas/{test_user.id}")
        assert response.status_code == status.HTTP_200_OK
    
    # Try to make one more request
    response = client.get(f"/api/v1/pessoas/{test_user.id}")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    
    # Check error response
    data = response.json()
    assert data["success"] is False
    assert "Too many requests" in data["error"]


def test_cors_middleware(client):
    """Test CORS middleware."""
    # Make a request with CORS headers
    response = client.options(
        "/api/v1/pessoas/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    
    # Check CORS headers
    assert response.status_code == status.HTTP_200_OK
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers 