import pytest
from datetime import datetime, timedelta
from app.core.validators import (
    BaseValidator,
    DateRangeValidator,
    PaginationValidator,
    SearchValidator,
    validate_required_fields,
    validate_unique_fields
)
from app.core.exceptions import ValidationException


def test_date_range_validator():
    """Test date range validation."""
    # Valid date range
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1)
    validator = DateRangeValidator(
        start_date=start_date,
        end_date=end_date
    )
    assert validator.start_date == start_date
    assert validator.end_date == end_date
    
    # Invalid date range
    with pytest.raises(ValidationException):
        DateRangeValidator(
            start_date=end_date,
            end_date=start_date
        )


def test_pagination_validator():
    """Test pagination validation."""
    # Valid pagination
    validator = PaginationValidator(page=1, page_size=10)
    assert validator.page == 1
    assert validator.page_size == 10
    
    # Invalid page
    with pytest.raises(ValidationException):
        PaginationValidator(page=0, page_size=10)
    
    # Invalid page size
    with pytest.raises(ValidationException):
        PaginationValidator(page=1, page_size=0)
    
    # Page size too large
    with pytest.raises(ValidationException):
        PaginationValidator(page=1, page_size=101)


def test_search_validator():
    """Test search validation."""
    # Valid search
    validator = SearchValidator(query="test")
    assert validator.query == "test"
    assert validator.fields is None
    
    # Valid search with fields
    validator = SearchValidator(
        query="test",
        fields=["title", "author"]
    )
    assert validator.query == "test"
    assert validator.fields == ["title", "author"]
    
    # Empty query
    with pytest.raises(ValidationException):
        SearchValidator(query="")
    
    # Query too long
    with pytest.raises(ValidationException):
        SearchValidator(query="x" * 101)


def test_validate_required_fields():
    """Test required fields validation."""
    # Valid data
    data = {
        "name": "John",
        "email": "john@example.com",
        "age": 30
    }
    required_fields = ["name", "email"]
    validate_required_fields(data, required_fields)
    
    # Missing required field
    with pytest.raises(ValidationException):
        validate_required_fields(
            {"name": "John"},
            ["name", "email"]
        )
    
    # None value
    with pytest.raises(ValidationException):
        validate_required_fields(
            {"name": "John", "email": None},
            ["name", "email"]
        )


def test_validate_unique_fields():
    """Test unique fields validation."""
    # Valid data
    data = {
        "name": "John",
        "email": "john@example.com",
        "age": 30
    }
    unique_fields = ["name", "email"]
    validate_unique_fields(data, unique_fields)
    
    # Invalid field type
    with pytest.raises(ValidationException):
        validate_unique_fields(
            {"name": ["John"]},
            ["name"]
        )
    
    # Complex object
    with pytest.raises(ValidationException):
        validate_unique_fields(
            {"name": {"first": "John"}},
            ["name"]
        ) 