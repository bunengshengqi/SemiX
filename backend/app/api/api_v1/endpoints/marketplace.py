from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.marketplace_service import MarketplaceService
from app.schemas.marketplace import (
    MarketplaceListing, MarketplaceListingCreate, MarketplaceListingUpdate,
    MarketplaceListingQuery, MarketplaceStats, MarketplaceListingSummary,
    MarketplaceInquiryCreate, MarketplaceInquiry, MarketplaceFavoriteCreate,
    MarketplaceFavorite, MarketplaceReportCreate
)
from app.models.user import User as UserModel
from app.models.marketplace import (
    ListingType, ListingStatus, ProductCondition, PriceType
)

router = APIRouter()

@router.get("/", response_model=List[MarketplaceListing])
async def get_marketplace_listings(
    listing_type: Optional[ListingType] = Query(None, description="交易类型"),
    status: Optional[ListingStatus] = Query(None, description="状态"),
    category: Optional[str] = Query(None, description="产品分类"),
    manufacturer: Optional[str] = Query(None, description="制造商"),
    condition: Optional[ProductCondition] = Query(None, description="产品条件"),
    price_type: Optional[PriceType] = Query(None, description="价格类型"),
    country: Optional[str] = Query(None, description="国家"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    min_price: Optional[float] = Query(None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(None, ge=0, description="最高价格"),
    is_verified: Optional[bool] = Query(None, description="是否已验证"),
    is_featured: Optional[bool] = Query(None, description="是否推荐"),
    is_urgent: Optional[bool] = Query(None, description="是否紧急"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取交易信息列表 - 公开访问"""
    query = MarketplaceListingQuery(
        listing_type=listing_type,
        status=status,
        category=category,
        manufacturer=manufacturer,
        condition=condition,
        price_type=price_type,
        country=country,
        keyword=keyword,
        min_price=min_price,
        max_price=max_price,
        is_verified=is_verified,
        is_featured=is_featured,
        is_urgent=is_urgent,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return MarketplaceService.get_listings_list(db, query)

@router.get("/stats", response_model=MarketplaceStats)
async def get_marketplace_stats(db: Session = Depends(get_db)):
    """获取交易市场统计信息 - 公开访问"""
    return MarketplaceService.get_marketplace_stats(db)

@router.get("/featured", response_model=List[MarketplaceListing])
async def get_featured_listings(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取推荐交易信息 - 公开访问"""
    return MarketplaceService.get_featured_listings(db, limit)

@router.get("/urgent", response_model=List[MarketplaceListing])
async def get_urgent_listings(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取紧急交易信息 - 公开访问"""
    return MarketplaceService.get_urgent_listings(db, limit)

@router.get("/latest", response_model=List[MarketplaceListing])
async def get_latest_listings(
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取最新交易信息 - 公开访问"""
    return MarketplaceService.get_latest_listings(db, limit)

@router.get("/search", response_model=List[MarketplaceListing])
async def search_listings(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索交易信息 - 公开访问"""
    return MarketplaceService.search_listings(db, q, limit)

@router.get("/{listing_id}", response_model=MarketplaceListing)
async def get_listing_detail(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """获取交易信息详情 - 公开访问"""
    listing = MarketplaceService.get_listing_by_id(db, listing_id)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易信息不存在"
        )
    
    # 增加浏览次数
    MarketplaceService.increment_view_count(db, listing_id)
    
    return listing

@router.post("/", response_model=MarketplaceListing, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_data: MarketplaceListingCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建交易信息（需要登录）"""
    return MarketplaceService.create_listing(db, listing_data, current_user.id)

@router.put("/{listing_id}", response_model=MarketplaceListing)
async def update_listing(
    listing_id: int,
    listing_update: MarketplaceListingUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新交易信息（仅创建者）"""
    listing = MarketplaceService.update_listing(db, listing_id, listing_update, current_user.id)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易信息不存在或无权限修改"
        )
    return listing

@router.delete("/{listing_id}")
async def delete_listing(
    listing_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除交易信息（仅创建者）"""
    success = MarketplaceService.delete_listing(db, listing_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易信息不存在或无权限删除"
        )
    return {"message": "交易信息删除成功"}

@router.post("/{listing_id}/inquiries", response_model=MarketplaceInquiry)
async def create_inquiry(
    listing_id: int,
    inquiry_data: MarketplaceInquiryCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建询价（需要登录）"""
    inquiry_data.listing_id = listing_id
    return MarketplaceService.create_inquiry(db, inquiry_data, current_user.id)

@router.post("/{listing_id}/favorites", response_model=MarketplaceFavorite)
async def add_to_favorites(
    listing_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """添加到收藏（需要登录）"""
    favorite_data = MarketplaceFavoriteCreate(listing_id=listing_id)
    return MarketplaceService.add_to_favorites(db, favorite_data, current_user.id)

@router.get("/my/listings", response_model=List[MarketplaceListing])
async def get_my_listings(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取我的交易信息（需要登录）"""
    query = MarketplaceListingQuery(skip=0, limit=100)
    # 这里需要在服务层添加按用户筛选的功能
    return []  # 临时返回空列表

@router.get("/my/favorites", response_model=List[MarketplaceListing])
async def get_my_favorites(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取我的收藏（需要登录）"""
    # 这里需要在服务层添加获取用户收藏的功能
    return []  # 临时返回空列表

@router.post("/reports", response_model=dict)
async def report_listing(
    report_data: MarketplaceReportCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """举报交易信息（需要登录）"""
    # 这里需要在服务层添加举报功能
    return {"message": "举报已提交，我们会尽快处理"}

# 管理员专用接口
@router.patch("/{listing_id}/verify")
async def verify_listing(
    listing_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """验证交易信息（仅管理员）"""
    listing_update = MarketplaceListingUpdate(is_verified=True)
    listing = MarketplaceService.update_listing(db, listing_id, listing_update)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易信息不存在"
        )
    return {"message": "交易信息已验证"}

@router.patch("/{listing_id}/feature")
async def feature_listing(
    listing_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """推荐交易信息（仅管理员）"""
    listing_update = MarketplaceListingUpdate(is_featured=True)
    listing = MarketplaceService.update_listing(db, listing_id, listing_update)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易信息不存在"
        )
    return {"message": "交易信息已设为推荐"}
