from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """创建新用户"""
        # 验证密码匹配
        if user_create.password != user_create.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码和确认密码不匹配"
            )
        
        # 检查邮箱是否已存在
        if UserService.get_user_by_email(db, user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )
        
        # 检查用户名是否已存在
        if UserService.get_user_by_username(db, user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被使用"
            )
        
        # 创建用户
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            company=user_create.company,
            phone=user_create.phone,
            user_type=user_create.user_type,
            industry=user_create.industry,
            position=user_create.position,
            country=user_create.country,
            region=user_create.region,
            bio=user_create.bio,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """验证用户登录"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.commit()
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
