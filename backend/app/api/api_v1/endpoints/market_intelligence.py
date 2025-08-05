from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.market_intelligence_service import MarketIntelligenceService
from app.schemas.market_intelligence import (
    MarketIntelligence, MarketIntelligenceCreate, MarketIntelligenceUpdate,
    MarketIntelligenceQuery, MarketIntelligenceStats, MarketIntelligenceSummary,
    IntelligenceCommentCreate, IntelligenceComment, IntelligenceViewCreate
)
from app.models.user import User as UserModel
from app.models.market_intelligence import (
    IntelligenceType, IntelligencePriority, IntelligenceStatus, MarketRegion
)

router = APIRouter()

@router.get("/", response_model=List[MarketIntelligence])
async def get_market_intelligence(
    intelligence_type: Optional[IntelligenceType] = Query(None, description="情报类型"),
    priority: Optional[IntelligencePriority] = Query(None, description="优先级"),
    status: Optional[IntelligenceStatus] = Query(None, description="状态"),
    region: Optional[MarketRegion] = Query(None, description="地区"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    author: Optional[str] = Query(None, description="作者"),
    organization: Optional[str] = Query(None, description="发布机构"),
    is_featured: Optional[bool] = Query(None, description="是否精选"),
    is_trending: Optional[bool] = Query(None, description="是否热门"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取市场情报列表 - 公开访问"""
    query = MarketIntelligenceQuery(
        intelligence_type=intelligence_type,
        priority=priority,
        status=status,
        region=region,
        keyword=keyword,
        author=author,
        organization=organization,
        is_featured=is_featured,
        is_trending=is_trending,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return MarketIntelligenceService.get_intelligence_list(db, query)

@router.get("/stats", response_model=MarketIntelligenceStats)
async def get_intelligence_stats(db: Session = Depends(get_db)):
    """获取市场情报统计信息 - 公开访问"""
    return MarketIntelligenceService.get_intelligence_stats(db)

@router.get("/featured", response_model=List[MarketIntelligence])
async def get_featured_intelligence(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取精选市场情报 - 公开访问"""
    return MarketIntelligenceService.get_featured_intelligence(db, limit)

@router.get("/trending", response_model=List[MarketIntelligence])
async def get_trending_intelligence(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取热门市场情报 - 公开访问"""
    return MarketIntelligenceService.get_trending_intelligence(db, limit)

@router.get("/latest", response_model=List[MarketIntelligence])
async def get_latest_intelligence(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取最新市场情报 - 公开访问"""
    return MarketIntelligenceService.get_latest_intelligence(db, limit)

@router.get("/search", response_model=List[MarketIntelligence])
async def search_intelligence(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索市场情报 - 公开访问"""
    return MarketIntelligenceService.search_intelligence(db, q, limit)

@router.get("/{intelligence_id}", response_model=MarketIntelligence)
async def get_intelligence_detail(
    intelligence_id: int,
    db: Session = Depends(get_db)
):
    """获取市场情报详情 - 公开访问"""
    intelligence = MarketIntelligenceService.get_intelligence_by_id(db, intelligence_id)
    if not intelligence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="市场情报不存在"
        )

    # 增加浏览次数
    MarketIntelligenceService.increment_view_count(db, intelligence_id)

    return intelligence

@router.post("/", response_model=MarketIntelligence, status_code=status.HTTP_201_CREATED)
async def create_intelligence(
    intelligence_data: MarketIntelligenceCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """创建市场情报（仅管理员）"""
    return MarketIntelligenceService.create_intelligence(db, intelligence_data, current_user.id)

@router.put("/{intelligence_id}", response_model=MarketIntelligence)
async def update_intelligence(
    intelligence_id: int,
    intelligence_update: MarketIntelligenceUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """更新市场情报（仅管理员）"""
    intelligence = MarketIntelligenceService.update_intelligence(db, intelligence_id, intelligence_update)
    if not intelligence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="市场情报不存在"
        )
    return intelligence

@router.delete("/{intelligence_id}")
async def delete_intelligence(
    intelligence_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """删除市场情报（仅管理员）"""
    success = MarketIntelligenceService.delete_intelligence(db, intelligence_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="市场情报不存在"
        )
    return {"message": "市场情报删除成功"}

@router.get("/reports")
async def get_market_reports(
    category: Optional[str] = Query(None, description="报告类别"),
    db: Session = Depends(get_db)
):
    """获取市场报告"""
    return {
        "message": "市场报告功能待实现",
        "category": category
    }
