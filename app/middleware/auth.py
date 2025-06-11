from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps
import os

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


class AuthHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a new JWT token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou expirado"
            )

    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> dict:
        """Get current user from token."""
        return self.verify_token(credentials.credentials)


# Decorator para proteção de rotas
def require_auth(roles: list = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object not found"
                )

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise HTTPException(
                    status_code=401,
                    detail="Token não fornecido"
                )

            try:
                token = auth_header.split(' ')[1]
                payload = AuthHandler().verify_token(token)
                
                if roles and payload.get('role') not in roles:
                    raise HTTPException(
                        status_code=403,
                        detail="Acesso não autorizado"
                    )
                
                request.state.user = payload
                return await func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(
                    status_code=401,
                    detail=str(e)
                )
        return wrapper
    return decorator 