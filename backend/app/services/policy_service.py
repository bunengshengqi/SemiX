from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.models.policy import Policy, PolicyUrgency, PolicyStatus, PolicyCategory
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyQuery, PolicyStats

class PolicyService:
    
    @staticmethod
    def create_policy(db: Session, policy_data: PolicyCreate, created_by: Optional[int] = None) -> Policy:
        """创建新政策"""
        db_policy = Policy(
            **policy_data.model_dump(),
            created_by=created_by
        )
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        return db_policy
    
    @staticmethod
    def get_policy_by_id(db: Session, policy_id: int) -> Optional[Policy]:
        """根据ID获取政策"""
        return db.query(Policy).filter(Policy.id == policy_id, Policy.is_active == True).first()
    
    @staticmethod
    def get_policies(db: Session, query: PolicyQuery) -> List[Policy]:
        """获取政策列表"""
        db_query = db.query(Policy).filter(Policy.is_active == True)
        
        # 应用过滤条件
        if query.country:
            db_query = db_query.filter(Policy.country == query.country)
        
        if query.category:
            db_query = db_query.filter(Policy.category == query.category)
        
        if query.urgency:
            db_query = db_query.filter(Policy.urgency == query.urgency)
        
        if query.status:
            db_query = db_query.filter(Policy.status == query.status)
        
        if query.keyword:
            keyword_filter = or_(
                Policy.title.contains(query.keyword),
                Policy.summary.contains(query.keyword),
                Policy.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(Policy, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(Policy, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_policy(db: Session, policy_id: int, policy_update: PolicyUpdate) -> Optional[Policy]:
        """更新政策"""
        db_policy = db.query(Policy).filter(Policy.id == policy_id, Policy.is_active == True).first()
        if not db_policy:
            return None
        
        update_data = policy_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_policy, field, value)
        
        db_policy.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_policy)
        return db_policy
    
    @staticmethod
    def delete_policy(db: Session, policy_id: int) -> bool:
        """软删除政策"""
        db_policy = db.query(Policy).filter(Policy.id == policy_id, Policy.is_active == True).first()
        if not db_policy:
            return False
        
        db_policy.is_active = False
        db_policy.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def get_policy_stats(db: Session) -> PolicyStats:
        """获取政策统计信息"""
        # 总政策数
        total_policies = db.query(Policy).filter(Policy.is_active == True).count()
        
        # 按国家统计
        by_country = {}
        country_stats = db.query(
            Policy.country, 
            func.count(Policy.id).label('count')
        ).filter(Policy.is_active == True).group_by(Policy.country).all()
        
        for country, count in country_stats:
            by_country[country] = count
        
        # 按分类统计
        by_category = {}
        category_stats = db.query(
            Policy.category, 
            func.count(Policy.id).label('count')
        ).filter(Policy.is_active == True).group_by(Policy.category).all()
        
        for category, count in category_stats:
            by_category[category.value] = count
        
        # 按紧急程度统计
        by_urgency = {}
        urgency_stats = db.query(
            Policy.urgency, 
            func.count(Policy.id).label('count')
        ).filter(Policy.is_active == True).group_by(Policy.urgency).all()
        
        for urgency, count in urgency_stats:
            by_urgency[urgency.value] = count
        
        # 最近7天更新的政策数
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_updates = db.query(Policy).filter(
            Policy.is_active == True,
            Policy.updated_at >= seven_days_ago
        ).count()
        
        return PolicyStats(
            total_policies=total_policies,
            by_country=by_country,
            by_category=by_category,
            by_urgency=by_urgency,
            recent_updates=recent_updates
        )
    
    @staticmethod
    def get_recent_policies(db: Session, limit: int = 10) -> List[Policy]:
        """获取最近的政策"""
        return db.query(Policy).filter(Policy.is_active == True)\
            .order_by(desc(Policy.created_at)).limit(limit).all()
    
    @staticmethod
    def get_high_impact_policies(db: Session, limit: int = 10) -> List[Policy]:
        """获取高影响政策"""
        return db.query(Policy).filter(
            Policy.is_active == True,
            Policy.impact_score >= 70
        ).order_by(desc(Policy.impact_score)).limit(limit).all()
    
    @staticmethod
    def search_policies(db: Session, search_term: str, limit: int = 20) -> List[Policy]:
        """搜索政策"""
        search_filter = or_(
            Policy.title.contains(search_term),
            Policy.summary.contains(search_term),
            Policy.content.contains(search_term),
            Policy.keywords.contains(search_term)
        )
        
        return db.query(Policy).filter(
            Policy.is_active == True,
            search_filter
        ).order_by(desc(Policy.created_at)).limit(limit).all()
