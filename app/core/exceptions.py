from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class BaseAPIException(HTTPException):
    """Base API exception."""
    
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Initialize base API exception.
        
        Args:
            status_code (int): HTTP status code.
            detail (Any, optional): Error detail. Defaults to None.
            headers (Optional[Dict[str, str]], optional): HTTP headers.
                Defaults to None.
        """
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )


class NotFoundException(BaseAPIException):
    """Resource not found exception."""
    
    def __init__(
        self,
        detail: str = "Resource not found"
    ) -> None:
        """Initialize not found exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Resource not found".
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ValidationException(BaseAPIException):
    """Validation error exception."""
    
    def __init__(
        self,
        detail: str = "Validation error"
    ) -> None:
        """Initialize validation exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Validation error".
        """
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class AuthenticationException(BaseAPIException):
    """Authentication error exception."""
    
    def __init__(
        self,
        detail: str = "Authentication failed"
    ) -> None:
        """Initialize authentication exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Authentication failed".
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationException(BaseAPIException):
    """Authorization error exception."""
    
    def __init__(
        self,
        detail: str = "Not enough permissions"
    ) -> None:
        """Initialize authorization exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Not enough permissions".
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ConflictException(BaseAPIException):
    """Resource conflict exception."""
    
    def __init__(
        self,
        detail: str = "Resource conflict"
    ) -> None:
        """Initialize conflict exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Resource conflict".
        """
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class BusinessRuleException(BaseAPIException):
    """Business rule violation exception."""
    
    def __init__(
        self,
        detail: str = "Business rule violation"
    ) -> None:
        """Initialize business rule exception.
        
        Args:
            detail (str, optional): Error detail.
                Defaults to "Business rule violation".
        """
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        ) 