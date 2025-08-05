from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.compliance_tool import (
    ComplianceTool, ToolUsageLog, ToolReview, ComplianceRegulation,
    ToolType, ToolCategory, ToolStatus, AccessLevel
)
from app.schemas.compliance_tool import (
    ComplianceToolCreate, ComplianceToolUpdate, ComplianceToolQuery,
    ComplianceToolStats, ToolUsageLogCreate, ToolReviewCreate
)

class ComplianceToolService:
    
    @staticmethod
    def create_tool(
        db: Session, 
        tool_data: ComplianceToolCreate, 
        created_by: Optional[int] = None
    ) -> ComplianceTool:
        """创建新的合规工具"""
        db_tool = ComplianceTool(
            **tool_data.model_dump(),
            created_by=created_by
        )
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool
    
    @staticmethod
    def get_tool_by_id(db: Session, tool_id: int) -> Optional[ComplianceTool]:
        """根据ID获取合规工具"""
        return db.query(ComplianceTool).filter(ComplianceTool.id == tool_id).first()
    
    @staticmethod
    def get_tools_list(db: Session, query: ComplianceToolQuery) -> List[ComplianceTool]:
        """获取合规工具列表"""
        db_query = db.query(ComplianceTool)
        
        # 应用过滤条件
        if query.tool_type:
            db_query = db_query.filter(ComplianceTool.tool_type == query.tool_type)
        
        if query.category:
            db_query = db_query.filter(ComplianceTool.category == query.category)
        
        if query.status:
            db_query = db_query.filter(ComplianceTool.status == query.status)
        
        if query.access_level:
            db_query = db_query.filter(ComplianceTool.access_level == query.access_level)
        
        if query.keyword:
            keyword_filter = or_(
                ComplianceTool.name.contains(query.keyword),
                ComplianceTool.description.contains(query.keyword),
                ComplianceTool.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        if query.vendor:
            db_query = db_query.filter(ComplianceTool.vendor.contains(query.vendor))
        
        if query.is_featured is not None:
            db_query = db_query.filter(ComplianceTool.is_featured == query.is_featured)
        
        if query.is_verified is not None:
            db_query = db_query.filter(ComplianceTool.is_verified == query.is_verified)
        
        if query.is_popular is not None:
            db_query = db_query.filter(ComplianceTool.is_popular == query.is_popular)
        
        if query.min_rating is not None:
            db_query = db_query.filter(ComplianceTool.rating >= query.min_rating)
        
        if query.max_price is not None:
            db_query = db_query.filter(ComplianceTool.price <= query.max_price)
        
        if query.trial_available is not None:
            db_query = db_query.filter(ComplianceTool.trial_available == query.trial_available)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(ComplianceTool, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(ComplianceTool, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_tool(
        db: Session, 
        tool_id: int, 
        tool_update: ComplianceToolUpdate
    ) -> Optional[ComplianceTool]:
        """更新合规工具"""
        db_tool = db.query(ComplianceTool).filter(ComplianceTool.id == tool_id).first()
        if not db_tool:
            return None
        
        update_data = tool_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tool, field, value)
        
        db_tool.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_tool)
        return db_tool
    
    @staticmethod
    def delete_tool(db: Session, tool_id: int) -> bool:
        """删除合规工具"""
        db_tool = db.query(ComplianceTool).filter(ComplianceTool.id == tool_id).first()
        if not db_tool:
            return False
        
        db.delete(db_tool)
        db.commit()
        return True
    
    @staticmethod
    def get_tool_stats(db: Session) -> ComplianceToolStats:
        """获取合规工具统计信息"""
        # 总工具数
        total_tools = db.query(ComplianceTool).count()
        
        # 按类型统计
        by_type = {}
        type_stats = db.query(
            ComplianceTool.tool_type,
            func.count(ComplianceTool.id).label('count')
        ).group_by(ComplianceTool.tool_type).all()
        
        for tool_type, count in type_stats:
            by_type[tool_type.value] = count
        
        # 按分类统计
        by_category = {}
        category_stats = db.query(
            ComplianceTool.category,
            func.count(ComplianceTool.id).label('count')
        ).group_by(ComplianceTool.category).all()
        
        for category, count in category_stats:
            by_category[category.value] = count
        
        # 按访问级别统计
        by_access_level = {}
        access_stats = db.query(
            ComplianceTool.access_level,
            func.count(ComplianceTool.id).label('count')
        ).group_by(ComplianceTool.access_level).all()
        
        for access_level, count in access_stats:
            by_access_level[access_level.value] = count
        
        # 按状态统计
        by_status = {}
        status_stats = db.query(
            ComplianceTool.status,
            func.count(ComplianceTool.id).label('count')
        ).group_by(ComplianceTool.status).all()
        
        for status, count in status_stats:
            by_status[status.value] = count
        
        # 推荐、验证、热门工具统计
        featured_count = db.query(ComplianceTool).filter(
            ComplianceTool.is_featured == True
        ).count()
        
        verified_count = db.query(ComplianceTool).filter(
            ComplianceTool.is_verified == True
        ).count()
        
        popular_count = db.query(ComplianceTool).filter(
            ComplianceTool.is_popular == True
        ).count()
        
        # 总使用量
        total_usage = db.query(func.sum(ComplianceTool.usage_count)).scalar() or 0
        
        # 平均评分
        avg_rating_result = db.query(func.avg(ComplianceTool.rating)).filter(
            ComplianceTool.rating > 0
        ).scalar()
        avg_rating = float(avg_rating_result) if avg_rating_result else 0.0
        
        return ComplianceToolStats(
            total_tools=total_tools,
            by_type=by_type,
            by_category=by_category,
            by_access_level=by_access_level,
            by_status=by_status,
            featured_count=featured_count,
            verified_count=verified_count,
            popular_count=popular_count,
            total_usage=total_usage,
            avg_rating=round(avg_rating, 2)
        )
    
    @staticmethod
    def get_featured_tools(db: Session, limit: int = 10) -> List[ComplianceTool]:
        """获取推荐合规工具"""
        return db.query(ComplianceTool).filter(
            ComplianceTool.is_featured == True,
            ComplianceTool.status == ToolStatus.ACTIVE
        ).order_by(desc(ComplianceTool.rating)).limit(limit).all()
    
    @staticmethod
    def get_popular_tools(db: Session, limit: int = 10) -> List[ComplianceTool]:
        """获取热门合规工具"""
        return db.query(ComplianceTool).filter(
            ComplianceTool.is_popular == True,
            ComplianceTool.status == ToolStatus.ACTIVE
        ).order_by(desc(ComplianceTool.usage_count)).limit(limit).all()
    
    @staticmethod
    def get_free_tools(db: Session, limit: int = 20) -> List[ComplianceTool]:
        """获取免费合规工具"""
        return db.query(ComplianceTool).filter(
            ComplianceTool.access_level == AccessLevel.FREE,
            ComplianceTool.status == ToolStatus.ACTIVE
        ).order_by(desc(ComplianceTool.rating)).limit(limit).all()
    
    @staticmethod
    def search_tools(db: Session, search_term: str, limit: int = 20) -> List[ComplianceTool]:
        """搜索合规工具"""
        search_filter = or_(
            ComplianceTool.name.contains(search_term),
            ComplianceTool.description.contains(search_term),
            ComplianceTool.keywords.contains(search_term)
        )
        
        return db.query(ComplianceTool).filter(
            ComplianceTool.status == ToolStatus.ACTIVE,
            search_filter
        ).order_by(desc(ComplianceTool.rating)).limit(limit).all()
    
    @staticmethod
    def get_tools_by_category(db: Session, category: ToolCategory, limit: int = 20) -> List[ComplianceTool]:
        """按分类获取合规工具"""
        return db.query(ComplianceTool).filter(
            ComplianceTool.category == category,
            ComplianceTool.status == ToolStatus.ACTIVE
        ).order_by(desc(ComplianceTool.rating)).limit(limit).all()
    
    @staticmethod
    def increment_usage_count(db: Session, tool_id: int) -> bool:
        """增加使用次数"""
        db_tool = db.query(ComplianceTool).filter(ComplianceTool.id == tool_id).first()
        if not db_tool:
            return False
        
        db_tool.usage_count += 1
        db.commit()
        return True
    
    @staticmethod
    def log_tool_usage(
        db: Session, 
        usage_data: ToolUsageLogCreate, 
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> ToolUsageLog:
        """记录工具使用日志"""
        db_log = ToolUsageLog(
            **usage_data.model_dump(),
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_log)
        
        # 增加工具使用次数
        ComplianceToolService.increment_usage_count(db, usage_data.tool_id)
        
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def add_tool_review(
        db: Session, 
        review_data: ToolReviewCreate, 
        user_id: Optional[int] = None
    ) -> ToolReview:
        """添加工具评价"""
        db_review = ToolReview(
            **review_data.model_dump(),
            user_id=user_id
        )
        db.add(db_review)
        
        # 更新工具评价数和平均评分
        db_tool = db.query(ComplianceTool).filter(
            ComplianceTool.id == review_data.tool_id
        ).first()
        if db_tool:
            db_tool.review_count += 1
            
            # 重新计算平均评分
            avg_rating = db.query(func.avg(ToolReview.rating)).filter(
                ToolReview.tool_id == review_data.tool_id
            ).scalar()
            if avg_rating:
                db_tool.rating = round(float(avg_rating), 1)
        
        db.commit()
        db.refresh(db_review)
        return db_review
