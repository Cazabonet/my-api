from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .config import get_settings
from .logging import get_logger
from .rate_limit import rate_limit_middleware

settings = get_settings()
logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response."""
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status={response.status_code}"
        )
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for error handling."""
    
    async def dispatch(self, request: Request, call_next):
        """Handle errors and log them."""
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise


def setup_middlewares(app):
    """Setup all middlewares."""
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS
    )
    
    # Logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Error handling middleware
    app.add_middleware(ErrorHandlingMiddleware)
    
    # Rate limiting middleware
    app.middleware("http")(rate_limit_middleware) 