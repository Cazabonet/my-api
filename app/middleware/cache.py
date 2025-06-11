from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Optional, Callable
import json
import redis
import os
from functools import wraps

# Configurações do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_EXPIRE = int(os.getenv("CACHE_EXPIRE", 300))  # 5 minutos


class CacheHandler:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

    def get_cache_key(self, request: Request) -> str:
        """Generate a unique cache key for the request."""
        return f"{request.method}:{request.url.path}:{request.query_params}"

    def get_cached_response(self, cache_key: str) -> Optional[Response]:
        """Get cached response if exists."""
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            return JSONResponse(
                content=json.loads(cached_data),
                status_code=200
            )
        return None

    def set_cached_response(
        self,
        cache_key: str,
        response: Response,
        expire: int = CACHE_EXPIRE
    ):
        """Cache the response."""
        if isinstance(response, JSONResponse):
            self.redis_client.setex(
                cache_key,
                expire,
                json.dumps(response.body)
            )


# Decorator para cache de respostas
def cache_response(expire: int = CACHE_EXPIRE):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                return await func(*args, **kwargs)

            # Não cachear requisições POST, PUT, DELETE
            if request.method not in ["GET"]:
                return await func(*args, **kwargs)

            cache_handler = CacheHandler()
            cache_key = cache_handler.get_cache_key(request)

            # Verificar cache
            cached_response = cache_handler.get_cached_response(cache_key)
            if cached_response:
                return cached_response

            # Executar função e cachear resposta
            response = await func(*args, **kwargs)
            cache_handler.set_cached_response(cache_key, response, expire)
            return response

        return wrapper
    return decorator


# Função para limpar cache
def clear_cache(pattern: str = "*"):
    """Clear cache entries matching the pattern."""
    cache_handler = CacheHandler()
    keys = cache_handler.redis_client.keys(pattern)
    if keys:
        cache_handler.redis_client.delete(*keys) 