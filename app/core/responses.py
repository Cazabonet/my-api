from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from .pagination import PageInfo, PaginatedResponse

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Base API response model."""
    success: bool
    message: str
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None


def success_response(
    message: str,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """Create success response."""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    error: str,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create error response."""
    return {
        "success": False,
        "error": error,
        "details": details
    }


def paginated_response(
    items: List[T],
    page: int = 1,
    page_size: Optional[int] = None
) -> Dict[str, Any]:
    """Create paginated response."""
    paginated = PaginatedResponse(
        items=items,
        page_info=PageInfo(
            current_page=page,
            page_size=page_size or 10,
            total_pages=len(items) // (page_size or 10) + 1,
            total_items=len(items),
            has_next=page < len(items) // (page_size or 10) + 1,
            has_previous=page > 1
        )
    )
    
    return success_response(
        message="Items retrieved successfully",
        data=paginated.dict()
    ) 