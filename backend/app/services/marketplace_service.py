from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.marketplace import (
    MarketplaceListing, MarketplaceInquiry, MarketplaceFavorite, 
    MarketplaceCategory, MarketplaceReport,
    ListingType, ListingStatus, ProductCondition, PriceType
)
from app.schemas.marketplace import (
    MarketplaceListingCreate, MarketplaceListingUpdate, MarketplaceListingQuery,
    MarketplaceStats, MarketplaceInquiryCreate, MarketplaceFavoriteCreate,
    MarketplaceCategoryCreate, MarketplaceReportCreate
)

class MarketplaceService:
    
    @staticmethod
    def create_listing(
        db: Session, 
        listing_data: MarketplaceListingCreate, 
        created_by: Optional[int] = None
    ) -> MarketplaceListing:
        """创建新的交易信息"""
        db_listing = MarketplaceListing(
            **listing_data.model_dump(),
            created_by=created_by
        )
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)
        return db_listing
    
    @staticmethod
    def get_listing_by_id(db: Session, listing_id: int) -> Optional[MarketplaceListing]:
        """根据ID获取交易信息"""
        return db.query(MarketplaceListing).filter(MarketplaceListing.id == listing_id).first()
    
    @staticmethod
    def get_listings_list(db: Session, query: MarketplaceListingQuery) -> List[MarketplaceListing]:
        """获取交易信息列表"""
        db_query = db.query(MarketplaceListing)
        
        # 应用过滤条件
        if query.listing_type:
            db_query = db_query.filter(MarketplaceListing.listing_type == query.listing_type)
        
        if query.status:
            db_query = db_query.filter(MarketplaceListing.status == query.status)
        else:
            # 默认只显示活跃的交易信息
            db_query = db_query.filter(MarketplaceListing.status == ListingStatus.ACTIVE)
        
        if query.category:
            db_query = db_query.filter(MarketplaceListing.category.contains(query.category))
        
        if query.manufacturer:
            db_query = db_query.filter(MarketplaceListing.manufacturer.contains(query.manufacturer))
        
        if query.condition:
            db_query = db_query.filter(MarketplaceListing.condition == query.condition)
        
        if query.price_type:
            db_query = db_query.filter(MarketplaceListing.price_type == query.price_type)
        
        if query.country:
            db_query = db_query.filter(MarketplaceListing.country.contains(query.country))
        
        if query.keyword:
            keyword_filter = or_(
                MarketplaceListing.title.contains(query.keyword),
                MarketplaceListing.description.contains(query.keyword),
                MarketplaceListing.product_name.contains(query.keyword),
                MarketplaceListing.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        if query.min_price is not None:
            db_query = db_query.filter(MarketplaceListing.price >= query.min_price)
        
        if query.max_price is not None:
            db_query = db_query.filter(MarketplaceListing.price <= query.max_price)
        
        if query.is_verified is not None:
            db_query = db_query.filter(MarketplaceListing.is_verified == query.is_verified)
        
        if query.is_featured is not None:
            db_query = db_query.filter(MarketplaceListing.is_featured == query.is_featured)
        
        if query.is_urgent is not None:
            db_query = db_query.filter(MarketplaceListing.is_urgent == query.is_urgent)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(MarketplaceListing, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(MarketplaceListing, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_listing(
        db: Session, 
        listing_id: int, 
        listing_update: MarketplaceListingUpdate,
        user_id: Optional[int] = None
    ) -> Optional[MarketplaceListing]:
        """更新交易信息"""
        db_listing = db.query(MarketplaceListing).filter(
            MarketplaceListing.id == listing_id
        ).first()
        if not db_listing:
            return None
        
        # 检查权限（只有创建者可以修改）
        if user_id and db_listing.created_by != user_id:
            return None
        
        update_data = listing_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_listing, field, value)
        
        db_listing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_listing)
        return db_listing
    
    @staticmethod
    def delete_listing(db: Session, listing_id: int, user_id: Optional[int] = None) -> bool:
        """删除交易信息"""
        db_listing = db.query(MarketplaceListing).filter(
            MarketplaceListing.id == listing_id
        ).first()
        if not db_listing:
            return False
        
        # 检查权限（只有创建者可以删除）
        if user_id and db_listing.created_by != user_id:
            return False
        
        # 软删除
        db_listing.status = ListingStatus.DELETED
        db.commit()
        return True
    
    @staticmethod
    def get_marketplace_stats(db: Session) -> MarketplaceStats:
        """获取交易市场统计信息"""
        # 总交易数
        total_listings = db.query(MarketplaceListing).count()
        
        # 活跃交易数
        active_listings = db.query(MarketplaceListing).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).count()
        
        # 按类型统计
        by_type = {}
        type_stats = db.query(
            MarketplaceListing.listing_type,
            func.count(MarketplaceListing.id).label('count')
        ).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).group_by(MarketplaceListing.listing_type).all()
        
        for listing_type, count in type_stats:
            by_type[listing_type.value] = count
        
        # 按分类统计
        by_category = {}
        category_stats = db.query(
            MarketplaceListing.category,
            func.count(MarketplaceListing.id).label('count')
        ).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE,
            MarketplaceListing.category.isnot(None)
        ).group_by(MarketplaceListing.category).all()
        
        for category, count in category_stats:
            by_category[category] = count
        
        # 按条件统计
        by_condition = {}
        condition_stats = db.query(
            MarketplaceListing.condition,
            func.count(MarketplaceListing.id).label('count')
        ).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).group_by(MarketplaceListing.condition).all()
        
        for condition, count in condition_stats:
            by_condition[condition.value] = count
        
        # 按国家统计
        by_country = {}
        country_stats = db.query(
            MarketplaceListing.country,
            func.count(MarketplaceListing.id).label('count')
        ).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).group_by(MarketplaceListing.country).all()
        
        for country, count in country_stats:
            by_country[country] = count
        
        # 推荐、验证、紧急交易统计
        featured_count = db.query(MarketplaceListing).filter(
            MarketplaceListing.is_featured == True,
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).count()
        
        verified_count = db.query(MarketplaceListing).filter(
            MarketplaceListing.is_verified == True,
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).count()
        
        urgent_count = db.query(MarketplaceListing).filter(
            MarketplaceListing.is_urgent == True,
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).count()
        
        # 总浏览量和询价量
        total_views = db.query(func.sum(MarketplaceListing.view_count)).scalar() or 0
        total_inquiries = db.query(func.sum(MarketplaceListing.inquiry_count)).scalar() or 0
        
        return MarketplaceStats(
            total_listings=total_listings,
            active_listings=active_listings,
            by_type=by_type,
            by_category=by_category,
            by_condition=by_condition,
            by_country=by_country,
            featured_count=featured_count,
            verified_count=verified_count,
            urgent_count=urgent_count,
            total_views=total_views,
            total_inquiries=total_inquiries
        )
    
    @staticmethod
    def get_featured_listings(db: Session, limit: int = 10) -> List[MarketplaceListing]:
        """获取推荐交易信息"""
        return db.query(MarketplaceListing).filter(
            MarketplaceListing.is_featured == True,
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).order_by(desc(MarketplaceListing.created_at)).limit(limit).all()
    
    @staticmethod
    def get_urgent_listings(db: Session, limit: int = 10) -> List[MarketplaceListing]:
        """获取紧急交易信息"""
        return db.query(MarketplaceListing).filter(
            MarketplaceListing.is_urgent == True,
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).order_by(desc(MarketplaceListing.created_at)).limit(limit).all()
    
    @staticmethod
    def get_latest_listings(db: Session, limit: int = 20) -> List[MarketplaceListing]:
        """获取最新交易信息"""
        return db.query(MarketplaceListing).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE
        ).order_by(desc(MarketplaceListing.created_at)).limit(limit).all()
    
    @staticmethod
    def search_listings(db: Session, search_term: str, limit: int = 20) -> List[MarketplaceListing]:
        """搜索交易信息"""
        search_filter = or_(
            MarketplaceListing.title.contains(search_term),
            MarketplaceListing.description.contains(search_term),
            MarketplaceListing.product_name.contains(search_term),
            MarketplaceListing.keywords.contains(search_term)
        )
        
        return db.query(MarketplaceListing).filter(
            MarketplaceListing.status == ListingStatus.ACTIVE,
            search_filter
        ).order_by(desc(MarketplaceListing.created_at)).limit(limit).all()
    
    @staticmethod
    def increment_view_count(db: Session, listing_id: int) -> bool:
        """增加浏览次数"""
        db_listing = db.query(MarketplaceListing).filter(
            MarketplaceListing.id == listing_id
        ).first()
        if not db_listing:
            return False
        
        db_listing.view_count += 1
        db.commit()
        return True
    
    @staticmethod
    def create_inquiry(
        db: Session, 
        inquiry_data: MarketplaceInquiryCreate, 
        user_id: Optional[int] = None
    ) -> MarketplaceInquiry:
        """创建询价"""
        db_inquiry = MarketplaceInquiry(
            **inquiry_data.model_dump(),
            created_by=user_id
        )
        db.add(db_inquiry)
        
        # 更新交易信息的询价数
        db_listing = db.query(MarketplaceListing).filter(
            MarketplaceListing.id == inquiry_data.listing_id
        ).first()
        if db_listing:
            db_listing.inquiry_count += 1
        
        db.commit()
        db.refresh(db_inquiry)
        return db_inquiry
    
    @staticmethod
    def add_to_favorites(
        db: Session, 
        favorite_data: MarketplaceFavoriteCreate, 
        user_id: int
    ) -> MarketplaceFavorite:
        """添加到收藏"""
        # 检查是否已收藏
        existing = db.query(MarketplaceFavorite).filter(
            MarketplaceFavorite.listing_id == favorite_data.listing_id,
            MarketplaceFavorite.user_id == user_id
        ).first()
        
        if existing:
            return existing
        
        db_favorite = MarketplaceFavorite(
            listing_id=favorite_data.listing_id,
            user_id=user_id
        )
        db.add(db_favorite)
        
        # 更新交易信息的收藏数
        db_listing = db.query(MarketplaceListing).filter(
            MarketplaceListing.id == favorite_data.listing_id
        ).first()
        if db_listing:
            db_listing.favorite_count += 1
        
        db.commit()
        db.refresh(db_favorite)
        return db_favorite
