from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.market_intelligence import (
    IntelligenceType, IntelligencePriority, IntelligenceStatus, MarketRegion
)

# 基础市场情报模式
class MarketIntelligenceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    subtitle: Optional[str] = Field(None, max_length=500)
    summary: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    intelligence_type: IntelligenceType
    priority: IntelligencePriority = IntelligencePriority.MEDIUM
    status: IntelligenceStatus = IntelligenceStatus.DRAFT
    region: MarketRegion = MarketRegion.GLOBAL
    industry_sectors: Optional[str] = None
    product_categories: Optional[str] = None
    market_size: Optional[float] = Field(None, ge=0)
    growth_rate: Optional[float] = None
    market_share: Optional[float] = Field(None, ge=0, le=100)
    price_change: Optional[float] = None
    report_date: datetime
    data_period_start: Optional[datetime] = None
    data_period_end: Optional[datetime] = None
    data_sources: Optional[str] = None
    author: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=200)
    tags: Optional[str] = None
    keywords: Optional[str] = None
    attachments: Optional[str] = None
    external_links: Optional[str] = None
    quality_score: float = Field(default=0.0, ge=0.0, le=5.0)
    relevance_score: float = Field(default=0.0, ge=0.0, le=5.0)
    timeliness_score: float = Field(default=0.0, ge=0.0, le=5.0)
    is_featured: bool = False
    is_trending: bool = False
    is_premium: bool = False
    is_verified: bool = False
    access_level: str = Field(default="public", max_length=50)

# 市场情报创建模式
class MarketIntelligenceCreate(MarketIntelligenceBase):
    pass

# 市场情报更新模式
class MarketIntelligenceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    subtitle: Optional[str] = Field(None, max_length=500)
    summary: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = Field(None, min_length=1)
    intelligence_type: Optional[IntelligenceType] = None
    priority: Optional[IntelligencePriority] = None
    status: Optional[IntelligenceStatus] = None
    region: Optional[MarketRegion] = None
    industry_sectors: Optional[str] = None
    product_categories: Optional[str] = None
    market_size: Optional[float] = Field(None, ge=0)
    growth_rate: Optional[float] = None
    market_share: Optional[float] = Field(None, ge=0, le=100)
    price_change: Optional[float] = None
    report_date: Optional[datetime] = None
    data_period_start: Optional[datetime] = None
    data_period_end: Optional[datetime] = None
    data_sources: Optional[str] = None
    author: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=200)
    tags: Optional[str] = None
    keywords: Optional[str] = None
    attachments: Optional[str] = None
    external_links: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=5.0)
    relevance_score: Optional[float] = Field(None, ge=0.0, le=5.0)
    timeliness_score: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_featured: Optional[bool] = None
    is_trending: Optional[bool] = None
    is_premium: Optional[bool] = None
    is_verified: Optional[bool] = None
    access_level: Optional[str] = Field(None, max_length=50)

# 数据库中的市场情报模式
class MarketIntelligenceInDB(MarketIntelligenceBase):
    id: int
    view_count: int
    like_count: int
    share_count: int
    comment_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的市场情报模式
class MarketIntelligence(MarketIntelligenceBase):
    id: int
    view_count: int
    like_count: int
    share_count: int
    comment_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 市场情报列表查询参数
class MarketIntelligenceQuery(BaseModel):
    intelligence_type: Optional[IntelligenceType] = None
    priority: Optional[IntelligencePriority] = None
    status: Optional[IntelligenceStatus] = None
    region: Optional[MarketRegion] = None
    keyword: Optional[str] = None
    author: Optional[str] = None
    organization: Optional[str] = None
    is_featured: Optional[bool] = None
    is_trending: Optional[bool] = None
    is_premium: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 市场情报统计模式
class MarketIntelligenceStats(BaseModel):
    total_intelligence: int
    by_type: dict
    by_region: dict
    by_priority: dict
    by_status: dict
    featured_count: int
    trending_count: int
    premium_count: int
    total_views: int
    avg_quality_score: float

# 市场情报简要信息（用于列表显示）
class MarketIntelligenceSummary(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    summary: str
    intelligence_type: IntelligenceType
    priority: IntelligencePriority
    region: MarketRegion
    author: Optional[str]
    organization: Optional[str]
    report_date: datetime
    view_count: int
    like_count: int
    quality_score: float
    is_featured: bool
    is_trending: bool
    is_premium: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 评论模式
class IntelligenceCommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    parent_id: Optional[int] = None

class IntelligenceCommentCreate(IntelligenceCommentBase):
    intelligence_id: int

class IntelligenceComment(IntelligenceCommentBase):
    id: int
    intelligence_id: int
    user_id: Optional[int]
    author_name: Optional[str]
    is_approved: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 浏览记录模式
class IntelligenceViewCreate(BaseModel):
    intelligence_id: int
    view_duration: Optional[int] = None

class IntelligenceView(BaseModel):
    id: int
    intelligence_id: int
    user_id: Optional[int]
    view_duration: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
