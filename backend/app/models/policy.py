from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
import enum

class PolicyUrgency(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PolicyStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    UPDATED = "updated"
    ARCHIVED = "archived"

class PolicyCategory(enum.Enum):
    EXPORT_CONTROL = "export_control"
    TRADE_POLICY = "trade_policy"
    INVESTMENT = "investment"
    TAXATION = "taxation"
    REGULATION = "regulation"
    COMPLIANCE = "compliance"

class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    
    # 地区信息
    country = Column(String(50), nullable=False, index=True)
    region = Column(String(100), nullable=True)
    
    # 政策分类
    category = Column(Enum(PolicyCategory), nullable=False, index=True)
    urgency = Column(Enum(PolicyUrgency), default=PolicyUrgency.MEDIUM, index=True)
    status = Column(Enum(PolicyStatus), default=PolicyStatus.PUBLISHED, index=True)
    
    # 政策详情
    policy_number = Column(String(100), nullable=True)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # 影响评估
    impact_score = Column(Integer, default=0)  # 0-100
    affected_industries = Column(Text, nullable=True)  # JSON格式存储
    
    # 来源信息
    source_url = Column(String(1000), nullable=True)
    source_name = Column(String(200), nullable=True)
    
    # 标签和关键词
    tags = Column(Text, nullable=True)  # JSON格式存储
    keywords = Column(Text, nullable=True)
    
    # 系统字段
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)  # 用户ID
    
    def __repr__(self):
        return f"<Policy(id={self.id}, title='{self.title[:50]}...', country='{self.country}')>"
