from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    """获取用户资料"""
    return {"message": "用户资料功能待实现"}

@router.put("/profile")
async def update_user_profile(db: Session = Depends(get_db)):
    """更新用户资料"""
    return {"message": "更新用户资料功能待实现"}

@router.get("/subscription")
async def get_subscription_info(db: Session = Depends(get_db)):
    """获取会员订阅信息"""
    return {"message": "会员订阅信息功能待实现"}
