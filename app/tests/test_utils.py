import pytest
from datetime import datetime, timedelta
from app.core.utils import (
    calculate_due_date,
    calculate_fine,
    format_datetime,
    parse_datetime,
    filter_dict,
    validate_business_rules,
    generate_reference_code
)
from app.core.exceptions import BusinessRuleException


def test_calculate_due_date():
    """Test due date calculation."""
    start_date = datetime.now()
    due_date = calculate_due_date(start_date)
    
    # Check if due date is 15 days after start date
    expected_due_date = start_date + timedelta(days=15)
    assert abs((due_date - expected_due_date).total_seconds()) < 1


def test_calculate_fine():
    """Test fine calculation."""
    due_date = datetime.now()
    
    # Return on time
    return_date = due_date
    fine = calculate_fine(due_date, return_date)
    assert fine == 0.0
    
    # Return 5 days late
    return_date = due_date + timedelta(days=5)
    fine = calculate_fine(due_date, return_date)
    assert fine == 5.0  # 5 days * 1.0 per day
    
    # Return 10 days late
    return_date = due_date + timedelta(days=10)
    fine = calculate_fine(due_date, return_date)
    assert fine == 10.0  # 10 days * 1.0 per day


def test_format_datetime():
    """Test datetime formatting."""
    dt = datetime(2024, 1, 1, 12, 0, 0)
    formatted = format_datetime(dt)
    assert formatted == "2024-01-01 12:00:00"


def test_parse_datetime():
    """Test datetime parsing."""
    dt_str = "2024-01-01 12:00:00"
    dt = parse_datetime(dt_str)
    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12
    assert dt.minute == 0
    assert dt.second == 0


def test_filter_dict():
    """Test dictionary filtering."""
    data = {
        "name": "John",
        "email": "john@example.com",
        "age": 30,
        "address": "123 Main St"
    }
    allowed_keys = ["name", "email"]
    
    filtered = filter_dict(data, allowed_keys)
    assert "name" in filtered
    assert "email" in filtered
    assert "age" not in filtered
    assert "address" not in filtered


def test_validate_business_rules():
    """Test business rules validation."""
    rules = {
        "max_loans": 3,
        "max_reservations": 2
    }
    context = {
        "max_loans": 3,
        "max_reservations": 2
    }
    
    # Valid rules
    validate_business_rules(rules, context)
    
    # Invalid rules
    with pytest.raises(BusinessRuleException):
        validate_business_rules(
            {"max_loans": 3},
            {"max_loans": 4}
        )
    
    # Missing context
    with pytest.raises(BusinessRuleException):
        validate_business_rules(
            {"max_loans": 3},
            {}
        )


def test_generate_reference_code():
    """Test reference code generation."""
    prefix = "TEST"
    code = generate_reference_code(prefix)
    
    # Check prefix
    assert code.startswith(prefix)
    
    # Check format
    assert len(code) == len(prefix) + 1 + 14  # prefix + "-" + timestamp
    
    # Check uniqueness
    code2 = generate_reference_code(prefix)
    assert code != code2 