from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .config import get_settings
from .exceptions import AuthenticationException
from .logging import get_logger
from app.database import get_db
from app.models.pessoa import Pessoa

settings = get_settings()
logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Pessoa:
    """Get current authenticated user."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise AuthenticationException("Invalid token")
    except JWTError:
        raise AuthenticationException("Invalid token")
    
    user = db.query(Pessoa).filter(Pessoa.id == user_id).first()
    if user is None:
        raise AuthenticationException("User not found")
    
    return user


def get_current_active_user(
    current_user: Pessoa = Depends(get_current_user)
) -> Pessoa:
    """Get current active user."""
    if not current_user.ativo:
        raise AuthenticationException("Inactive user")
    return current_user


def get_current_admin_user(
    current_user: Pessoa = Depends(get_current_active_user)
) -> Pessoa:
    """Get current admin user."""
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user 