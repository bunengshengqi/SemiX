from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.policy_service import PolicyService
from app.schemas.policy import Policy, PolicyCreate, PolicyUpdate, PolicyQuery, PolicyStats
from app.models.user import User as UserModel
from app.models.policy import PolicyUrgency, PolicyStatus, PolicyCategory

router = APIRouter()

@router.get("/", response_model=List[Policy])
async def get_policies(
    country: Optional[str] = Query(None, description="按国家过滤"),
    category: Optional[PolicyCategory] = Query(None, description="按分类过滤"),
    urgency: Optional[PolicyUrgency] = Query(None, description="按紧急程度过滤"),
    status: Optional[PolicyStatus] = Query(None, description="按状态过滤"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取政策列表 - 公开访问"""
    query = PolicyQuery(
        country=country,
        category=category,
        urgency=urgency,
        status=status,
        keyword=keyword,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return PolicyService.get_policies(db, query)

@router.get("/stats", response_model=PolicyStats)
async def get_policy_stats(db: Session = Depends(get_db)):
    """获取政策统计信息 - 公开访问"""
    return PolicyService.get_policy_stats(db)

@router.get("/recent", response_model=List[Policy])
async def get_recent_policies(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取最近的政策 - 公开访问"""
    return PolicyService.get_recent_policies(db, limit)

@router.get("/high-impact", response_model=List[Policy])
async def get_high_impact_policies(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取高影响政策"""
    return PolicyService.get_high_impact_policies(db, limit)

@router.get("/search", response_model=List[Policy])
async def search_policies(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索政策"""
    return PolicyService.search_policies(db, q, limit)

@router.get("/{policy_id}", response_model=Policy)
async def get_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    """获取单个政策详情"""
    policy = PolicyService.get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    return policy

@router.post("/", response_model=Policy, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_data: PolicyCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """创建新政策（仅管理员）"""
    return PolicyService.create_policy(db, policy_data, current_user.id)

@router.put("/{policy_id}", response_model=Policy)
async def update_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """更新政策（仅管理员）"""
    policy = PolicyService.update_policy(db, policy_id, policy_update)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    return policy

@router.delete("/{policy_id}")
async def delete_policy(
    policy_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """删除政策（仅管理员）"""
    success = PolicyService.delete_policy(db, policy_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    return {"message": "政策删除成功"}
