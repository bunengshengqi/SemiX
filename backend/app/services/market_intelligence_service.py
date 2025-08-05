from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.market_intelligence import (
    MarketIntelligence, IntelligenceComment, IntelligenceView,
    IntelligenceType, IntelligencePriority, IntelligenceStatus, MarketRegion
)
from app.schemas.market_intelligence import (
    MarketIntelligenceCreate, MarketIntelligenceUpdate, MarketIntelligenceQuery,
    MarketIntelligenceStats, IntelligenceCommentCreate, IntelligenceViewCreate
)

class MarketIntelligenceService:
    
    @staticmethod
    def create_intelligence(
        db: Session, 
        intelligence_data: MarketIntelligenceCreate, 
        created_by: Optional[int] = None
    ) -> MarketIntelligence:
        """创建新的市场情报"""
        db_intelligence = MarketIntelligence(
            **intelligence_data.model_dump(),
            created_by=created_by
        )
        db.add(db_intelligence)
        db.commit()
        db.refresh(db_intelligence)
        return db_intelligence
    
    @staticmethod
    def get_intelligence_by_id(db: Session, intelligence_id: int) -> Optional[MarketIntelligence]:
        """根据ID获取市场情报"""
        return db.query(MarketIntelligence).filter(MarketIntelligence.id == intelligence_id).first()
    
    @staticmethod
    def get_intelligence_list(db: Session, query: MarketIntelligenceQuery) -> List[MarketIntelligence]:
        """获取市场情报列表"""
        db_query = db.query(MarketIntelligence)
        
        # 应用过滤条件
        if query.intelligence_type:
            db_query = db_query.filter(MarketIntelligence.intelligence_type == query.intelligence_type)
        
        if query.priority:
            db_query = db_query.filter(MarketIntelligence.priority == query.priority)
        
        if query.status:
            db_query = db_query.filter(MarketIntelligence.status == query.status)
        
        if query.region:
            db_query = db_query.filter(MarketIntelligence.region == query.region)
        
        if query.keyword:
            keyword_filter = or_(
                MarketIntelligence.title.contains(query.keyword),
                MarketIntelligence.summary.contains(query.keyword),
                MarketIntelligence.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        if query.author:
            db_query = db_query.filter(MarketIntelligence.author.contains(query.author))
        
        if query.organization:
            db_query = db_query.filter(MarketIntelligence.organization.contains(query.organization))
        
        if query.is_featured is not None:
            db_query = db_query.filter(MarketIntelligence.is_featured == query.is_featured)
        
        if query.is_trending is not None:
            db_query = db_query.filter(MarketIntelligence.is_trending == query.is_trending)
        
        if query.is_premium is not None:
            db_query = db_query.filter(MarketIntelligence.is_premium == query.is_premium)
        
        if query.date_from:
            db_query = db_query.filter(MarketIntelligence.report_date >= query.date_from)
        
        if query.date_to:
            db_query = db_query.filter(MarketIntelligence.report_date <= query.date_to)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(MarketIntelligence, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(MarketIntelligence, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_intelligence(
        db: Session, 
        intelligence_id: int, 
        intelligence_update: MarketIntelligenceUpdate
    ) -> Optional[MarketIntelligence]:
        """更新市场情报"""
        db_intelligence = db.query(MarketIntelligence).filter(
            MarketIntelligence.id == intelligence_id
        ).first()
        if not db_intelligence:
            return None
        
        update_data = intelligence_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_intelligence, field, value)
        
        db_intelligence.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_intelligence)
        return db_intelligence
    
    @staticmethod
    def delete_intelligence(db: Session, intelligence_id: int) -> bool:
        """删除市场情报"""
        db_intelligence = db.query(MarketIntelligence).filter(
            MarketIntelligence.id == intelligence_id
        ).first()
        if not db_intelligence:
            return False
        
        db.delete(db_intelligence)
        db.commit()
        return True
    
    @staticmethod
    def get_intelligence_stats(db: Session) -> MarketIntelligenceStats:
        """获取市场情报统计信息"""
        # 总情报数
        total_intelligence = db.query(MarketIntelligence).count()
        
        # 按类型统计
        by_type = {}
        type_stats = db.query(
            MarketIntelligence.intelligence_type,
            func.count(MarketIntelligence.id).label('count')
        ).group_by(MarketIntelligence.intelligence_type).all()
        
        for intelligence_type, count in type_stats:
            by_type[intelligence_type.value] = count
        
        # 按地区统计
        by_region = {}
        region_stats = db.query(
            MarketIntelligence.region,
            func.count(MarketIntelligence.id).label('count')
        ).group_by(MarketIntelligence.region).all()
        
        for region, count in region_stats:
            by_region[region.value] = count
        
        # 按优先级统计
        by_priority = {}
        priority_stats = db.query(
            MarketIntelligence.priority,
            func.count(MarketIntelligence.id).label('count')
        ).group_by(MarketIntelligence.priority).all()
        
        for priority, count in priority_stats:
            by_priority[priority.value] = count
        
        # 按状态统计
        by_status = {}
        status_stats = db.query(
            MarketIntelligence.status,
            func.count(MarketIntelligence.id).label('count')
        ).group_by(MarketIntelligence.status).all()
        
        for status, count in status_stats:
            by_status[status.value] = count
        
        # 精选、热门、付费内容统计
        featured_count = db.query(MarketIntelligence).filter(
            MarketIntelligence.is_featured == True
        ).count()
        
        trending_count = db.query(MarketIntelligence).filter(
            MarketIntelligence.is_trending == True
        ).count()
        
        premium_count = db.query(MarketIntelligence).filter(
            MarketIntelligence.is_premium == True
        ).count()
        
        # 总浏览量
        total_views = db.query(func.sum(MarketIntelligence.view_count)).scalar() or 0
        
        # 平均质量评分
        avg_quality_result = db.query(func.avg(MarketIntelligence.quality_score)).filter(
            MarketIntelligence.quality_score > 0
        ).scalar()
        avg_quality_score = float(avg_quality_result) if avg_quality_result else 0.0
        
        return MarketIntelligenceStats(
            total_intelligence=total_intelligence,
            by_type=by_type,
            by_region=by_region,
            by_priority=by_priority,
            by_status=by_status,
            featured_count=featured_count,
            trending_count=trending_count,
            premium_count=premium_count,
            total_views=total_views,
            avg_quality_score=round(avg_quality_score, 2)
        )
    
    @staticmethod
    def get_featured_intelligence(db: Session, limit: int = 10) -> List[MarketIntelligence]:
        """获取精选市场情报"""
        return db.query(MarketIntelligence).filter(
            MarketIntelligence.is_featured == True,
            MarketIntelligence.status == IntelligenceStatus.PUBLISHED
        ).order_by(desc(MarketIntelligence.quality_score)).limit(limit).all()
    
    @staticmethod
    def get_trending_intelligence(db: Session, limit: int = 10) -> List[MarketIntelligence]:
        """获取热门市场情报"""
        return db.query(MarketIntelligence).filter(
            MarketIntelligence.is_trending == True,
            MarketIntelligence.status == IntelligenceStatus.PUBLISHED
        ).order_by(desc(MarketIntelligence.view_count)).limit(limit).all()
    
    @staticmethod
    def get_latest_intelligence(db: Session, limit: int = 10) -> List[MarketIntelligence]:
        """获取最新市场情报"""
        return db.query(MarketIntelligence).filter(
            MarketIntelligence.status == IntelligenceStatus.PUBLISHED
        ).order_by(desc(MarketIntelligence.published_at)).limit(limit).all()
    
    @staticmethod
    def search_intelligence(db: Session, search_term: str, limit: int = 20) -> List[MarketIntelligence]:
        """搜索市场情报"""
        search_filter = or_(
            MarketIntelligence.title.contains(search_term),
            MarketIntelligence.summary.contains(search_term),
            MarketIntelligence.content.contains(search_term),
            MarketIntelligence.keywords.contains(search_term)
        )
        
        return db.query(MarketIntelligence).filter(
            MarketIntelligence.status == IntelligenceStatus.PUBLISHED,
            search_filter
        ).order_by(desc(MarketIntelligence.relevance_score)).limit(limit).all()
    
    @staticmethod
    def increment_view_count(db: Session, intelligence_id: int) -> bool:
        """增加浏览次数"""
        db_intelligence = db.query(MarketIntelligence).filter(
            MarketIntelligence.id == intelligence_id
        ).first()
        if not db_intelligence:
            return False
        
        db_intelligence.view_count += 1
        db.commit()
        return True
    
    @staticmethod
    def add_comment(db: Session, comment_data: IntelligenceCommentCreate, user_id: Optional[int] = None) -> IntelligenceComment:
        """添加评论"""
        db_comment = IntelligenceComment(
            **comment_data.model_dump(),
            user_id=user_id
        )
        db.add(db_comment)
        
        # 更新情报的评论数
        db_intelligence = db.query(MarketIntelligence).filter(
            MarketIntelligence.id == comment_data.intelligence_id
        ).first()
        if db_intelligence:
            db_intelligence.comment_count += 1
        
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def record_view(db: Session, view_data: IntelligenceViewCreate, user_id: Optional[int] = None) -> IntelligenceView:
        """记录浏览"""
        db_view = IntelligenceView(
            **view_data.model_dump(),
            user_id=user_id
        )
        db.add(db_view)
        db.commit()
        db.refresh(db_view)
        return db_view
