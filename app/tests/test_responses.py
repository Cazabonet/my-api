from app.core.responses import (
    APIResponse,
    ErrorResponse,
    success_response,
    error_response,
    paginated_response
)


def test_api_response():
    """Test API response model."""
    # Test with data
    response = APIResponse(
        success=True,
        message="Success",
        data={"id": 1, "name": "Test"}
    )
    assert response.success is True
    assert response.message == "Success"
    assert response.data == {"id": 1, "name": "Test"}
    
    # Test without data
    response = APIResponse(
        success=True,
        message="Success"
    )
    assert response.success is True
    assert response.message == "Success"
    assert response.data is None


def test_error_response():
    """Test error response model."""
    response = ErrorResponse(
        error="Test error",
        details={"field": "value"}
    )
    assert response.success is False
    assert response.error == "Test error"
    assert response.details == {"field": "value"}


def test_success_response():
    """Test success response function."""
    # Test with data
    response = success_response(
        message="Success",
        data={"id": 1, "name": "Test"}
    )
    assert response["success"] is True
    assert response["message"] == "Success"
    assert response["data"] == {"id": 1, "name": "Test"}
    
    # Test without data
    response = success_response(message="Success")
    assert response["success"] is True
    assert response["message"] == "Success"
    assert response["data"] is None


def test_error_response_function():
    """Test error response function."""
    # Test with details
    response = error_response(
        error="Test error",
        details={"field": "value"}
    )
    assert response["success"] is False
    assert response["error"] == "Test error"
    assert response["details"] == {"field": "value"}
    
    # Test without details
    response = error_response(error="Test error")
    assert response["success"] is False
    assert response["error"] == "Test error"
    assert response["details"] is None


def test_paginated_response():
    """Test paginated response function."""
    items = [{"id": i, "name": f"Item {i}"} for i in range(1, 11)]
    
    # Test first page
    response = paginated_response(items, page=1, page_size=5)
    assert response["success"] is True
    assert response["message"] == "Items retrieved successfully"
    assert len(response["data"]["items"]) == 5
    assert response["data"]["page_info"]["current_page"] == 1
    assert response["data"]["page_info"]["page_size"] == 5
    assert response["data"]["page_info"]["total_pages"] == 2
    assert response["data"]["page_info"]["total_items"] == 10
    assert response["data"]["page_info"]["has_next"] is True
    assert response["data"]["page_info"]["has_previous"] is False
    
    # Test second page
    response = paginated_response(items, page=2, page_size=5)
    assert response["success"] is True
    assert response["message"] == "Items retrieved successfully"
    assert len(response["data"]["items"]) == 5
    assert response["data"]["page_info"]["current_page"] == 2
    assert response["data"]["page_info"]["page_size"] == 5
    assert response["data"]["page_info"]["total_pages"] == 2
    assert response["data"]["page_info"]["total_items"] == 10
    assert response["data"]["page_info"]["has_next"] is False
    assert response["data"]["page_info"]["has_previous"] is True
    
    # Test empty items
    response = paginated_response([], page=1, page_size=5)
    assert response["success"] is True
    assert response["message"] == "Items retrieved successfully"
    assert len(response["data"]["items"]) == 0
    assert response["data"]["page_info"]["current_page"] == 1
    assert response["data"]["page_info"]["page_size"] == 5
    assert response["data"]["page_info"]["total_pages"] == 0
    assert response["data"]["page_info"]["total_items"] == 0
    assert response["data"]["page_info"]["has_next"] is False
    assert response["data"]["page_info"]["has_previous"] is False 