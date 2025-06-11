from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, validator
from .exceptions import ValidationException


class BaseValidator(BaseModel):
    """Base validator model."""
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
        validate_assignment = True


class DateRangeValidator(BaseValidator):
    """Date range validator."""
    start_date: datetime
    end_date: datetime
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Validate date range."""
        if 'start_date' in values and v < values['start_date']:
            raise ValidationException(
                "End date must be greater than start date"
            )
        return v


class PaginationValidator(BaseValidator):
    """Pagination validator."""
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)


class SearchValidator(BaseValidator):
    """Search validator."""
    query: str = Field(..., min_length=1, max_length=100)
    fields: Optional[list[str]] = None


def validate_required_fields(
    data: Dict[str, Any],
    required_fields: list[str]
) -> None:
    """Validate required fields."""
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] is None
    ]
    
    if missing_fields:
        raise ValidationException(
            f"Missing required fields: {', '.join(missing_fields)}"
        )


def validate_unique_fields(
    data: Dict[str, Any],
    unique_fields: list[str]
) -> None:
    """Validate unique fields."""
    for field in unique_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], (str, int, float)):
                raise ValidationException(
                    f"Field {field} must be a string, number or float"
                ) 