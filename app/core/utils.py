from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from .constants import BUSINESS_RULES
from .exceptions import BusinessRuleException


def calculate_due_date(start_date: datetime) -> datetime:
    """Calculate due date for a loan."""
    return start_date + timedelta(days=BUSINESS_RULES["LOAN_DURATION_DAYS"])


def calculate_fine(due_date: datetime, return_date: datetime) -> float:
    """Calculate fine for overdue return."""
    if return_date <= due_date:
        return 0.0
    
    days_overdue = (return_date - due_date).days
    return days_overdue * BUSINESS_RULES["OVERDUE_FINE_PER_DAY"]


def format_datetime(dt: datetime) -> str:
    """Format datetime to string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(dt_str: str) -> datetime:
    """Parse string to datetime."""
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")


def filter_dict(
    data: Dict[str, Any],
    allowed_keys: List[str]
) -> Dict[str, Any]:
    """Filter dictionary to include only allowed keys."""
    return {
        key: value for key, value in data.items()
        if key in allowed_keys
    }


def validate_business_rules(
    rules: Dict[str, Any],
    context: Dict[str, Any]
) -> None:
    """Validate business rules."""
    for rule, value in rules.items():
        if rule not in context:
            raise BusinessRuleException(f"Missing context for rule: {rule}")
        
        if context[rule] != value:
            raise BusinessRuleException(
                f"Business rule violation: {rule}"
            )


def generate_reference_code(prefix: str) -> str:
    """Generate unique reference code."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}" 