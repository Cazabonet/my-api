from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field
from .config import get_settings

settings = get_settings()

T = TypeVar('T')


class PageInfo(BaseModel):
    """Pagination information."""
    
    current_page: int = Field(
        default=1,
        description="Current page number"
    )
    page_size: int = Field(
        default=10,
        description="Number of items per page"
    )
    total_pages: int = Field(
        default=0,
        description="Total number of pages"
    )
    total_items: int = Field(
        default=0,
        description="Total number of items"
    )
    has_next: bool = Field(
        default=False,
        description="Whether there is a next page"
    )
    has_previous: bool = Field(
        default=False,
        description="Whether there is a previous page"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    
    items: List[T] = Field(
        default_factory=list,
        description="List of items in the current page"
    )
    page_info: PageInfo = Field(
        description="Pagination information"
    )


def paginate(
    items: List[T],
    page: int = 1,
    page_size: int = 10
) -> PaginatedResponse[T]:
    """Paginate a list of items.
    
    Args:
        items (List[T]): List of items to paginate.
        page (int, optional): Page number. Defaults to 1.
        page_size (int, optional): Items per page. Defaults to 10.
        
    Returns:
        PaginatedResponse[T]: Paginated response.
    """
    # Calculate pagination values
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    # Adjust page number if out of range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # Calculate slice indices
    start = (page - 1) * page_size
    end = start + page_size
    
    # Get items for current page
    page_items = items[start:end]
    
    # Create page info
    page_info = PageInfo(
        current_page=page,
        page_size=page_size,
        total_pages=total_pages,
        total_items=total_items,
        has_next=page < total_pages,
        has_previous=page > 1
    )
    
    return PaginatedResponse(items=page_items, page_info=page_info) 