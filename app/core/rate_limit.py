import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
import logging

from app.core.config import settings


class RateLimiter:
    """Rate limiter implementation."""
    
    def __init__(self) -> None:
        """Initialize rate limiter."""
        self.requests: Dict[str, list] = {}
        self.logger = logging.getLogger("library_api")
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request.
        
        Args:
            request (Request): FastAPI request object.
            
        Returns:
            str: Client identifier.
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"
    
    def _cleanup_old_requests(self, client_id: str) -> None:
        """Remove expired requests from client history.
        
        Args:
            client_id (str): Client identifier.
        """
        current_time = time.time()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ]
    
    def check_rate_limit(self, request: Request) -> Tuple[bool, int]:
        """Check if request is within rate limits.
        
        Args:
            request (Request): FastAPI request object.
            
        Returns:
            Tuple[bool, int]: (is_allowed, remaining_requests)
            
        Raises:
            HTTPException: If rate limit is exceeded.
        """
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        # Initialize client request history
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean up old requests
        self._cleanup_old_requests(client_id)
        
        # Check rate limit
        if len(self.requests[client_id]) >= settings.RATE_LIMIT_PER_MINUTE:
            self.logger.warning(
                f"Rate limit exceeded for client {client_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        # Add current request
        self.requests[client_id].append(current_time)
        
        # Calculate remaining requests
        remaining = settings.RATE_LIMIT_PER_MINUTE - len(
            self.requests[client_id]
        )
        
        return True, remaining


# Create rate limiter instance
rate_limiter = RateLimiter() 