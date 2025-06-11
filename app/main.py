from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.pessoa import pessoa_router
from middleware.logging import LoggingMiddleware, RequestLogger
from middleware.cache import cache_response
from middleware.auth import require_auth
import time

app = FastAPI(
    title="Biblioteca API",
    description="API para gerenciamento de biblioteca",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middleware de logging
app.add_middleware(LoggingMiddleware)

# Middleware para adicionar request_id
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(time.time()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    RequestLogger.log_request(request)
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        RequestLogger.log_response(response, process_time)
        return response
    except Exception as e:
        RequestLogger.log_error(e, request)
        raise

# Rotas
app.include_router(pessoa_router)

# Rota de health check
@app.get("/health")
@cache_response(expire=60)  # Cache por 1 minuto
async def health_check():
    return {"status": "healthy"}

# Rota protegida de exemplo
@app.get("/protected")
@require_auth(roles=["admin"])
async def protected_route():
    return {"message": "Rota protegida acessada com sucesso"} 