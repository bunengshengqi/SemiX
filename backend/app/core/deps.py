from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import verify_token
from app.services.user_service import UserService
from app.models.user import User

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserService.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="用户账户已被禁用"
        )
    return current_user

def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前已验证用户"""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户邮箱未验证"
        )
    return current_user

def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user

def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（用于可选认证的端点）"""
    if token is None:
        return None
    
    try:
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        
        user = UserService.get_user_by_id(db, user_id=user_id)
        return user if user and user.is_active else None
    except JWTError:
        return None
