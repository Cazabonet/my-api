from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import json
import logging
from datetime import datetime
import os

# Configuração do logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Configurar logger
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Tempo inicial
        start_time = time.time()

        # Log da requisição
        request_id = request.headers.get("X-Request-ID", "N/A")
        logger.info(
            f"Request started - ID: {request_id} - "
            f"Method: {request.method} - "
            f"Path: {request.url.path}"
        )

        # Log do corpo da requisição (se houver)
        try:
            body = await request.body()
            if body:
                logger.debug(
                    f"Request body - ID: {request_id} - "
                    f"Body: {body.decode()}"
                )
        except Exception as e:
            logger.error(f"Error reading request body: {str(e)}")

        # Processar a requisição
        try:
            response = await call_next(request)
            
            # Calcular tempo de processamento
            process_time = time.time() - start_time
            
            # Log da resposta
            logger.info(
                f"Request completed - ID: {request_id} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.2f}s"
            )

            # Adicionar headers de logging
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # Log de erro
            logger.error(
                f"Request failed - ID: {request_id} - "
                f"Error: {str(e)}"
            )
            raise


class RequestLogger:
    @staticmethod
    def log_request(request: Request):
        """Log detailed request information."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request.headers.get("X-Request-ID", "N/A"),
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_host": request.client.host if request.client else "N/A",
            "headers": dict(request.headers)
        }
        logger.info(f"Request details: {json.dumps(log_data)}")

    @staticmethod
    def log_response(response: Response, process_time: float):
        """Log detailed response information."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": response.headers.get("X-Request-ID", "N/A"),
            "status_code": response.status_code,
            "process_time": process_time,
            "headers": dict(response.headers)
        }
        logger.info(f"Response details: {json.dumps(log_data)}")

    @staticmethod
    def log_error(error: Exception, request: Request):
        """Log error information."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request.headers.get("X-Request-ID", "N/A"),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "path": request.url.path,
            "method": request.method
        }
        logger.error(f"Error details: {json.dumps(log_data)}") 