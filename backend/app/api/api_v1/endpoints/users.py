from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.user_service import UserService
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel

router = APIRouter()

@router.get("/profile", response_model=User)
async def get_user_profile(
    current_user: UserModel = Depends(get_current_active_user)
):
    """获取当前用户资料"""
    return current_user

@router.put("/profile", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新当前用户资料"""
    updated_user = UserService.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return updated_user

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """获取用户列表（仅超级用户）"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """根据ID获取用户（仅超级用户）"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@router.get("/subscription")
async def get_subscription_info(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取会员订阅信息"""
    return {"message": "会员订阅信息功能待实现", "user_id": current_user.id}
