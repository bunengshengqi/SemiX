from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.policy import PolicyUrgency, PolicyStatus, PolicyCategory

# 基础政策模式
class PolicyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    summary: str = Field(..., min_length=1)
    content: Optional[str] = None
    country: str = Field(..., min_length=1, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    category: PolicyCategory
    urgency: PolicyUrgency = PolicyUrgency.MEDIUM
    status: PolicyStatus = PolicyStatus.PUBLISHED
    policy_number: Optional[str] = Field(None, max_length=100)
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    impact_score: int = Field(default=0, ge=0, le=100)
    affected_industries: Optional[str] = None  # JSON字符串
    source_url: Optional[str] = Field(None, max_length=1000)
    source_name: Optional[str] = Field(None, max_length=200)
    tags: Optional[str] = None  # JSON字符串
    keywords: Optional[str] = None
    is_active: bool = True

# 政策创建模式
class PolicyCreate(PolicyBase):
    pass

# 政策更新模式
class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    summary: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = None
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    category: Optional[PolicyCategory] = None
    urgency: Optional[PolicyUrgency] = None
    status: Optional[PolicyStatus] = None
    policy_number: Optional[str] = Field(None, max_length=100)
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    impact_score: Optional[int] = Field(None, ge=0, le=100)
    affected_industries: Optional[str] = None
    source_url: Optional[str] = Field(None, max_length=1000)
    source_name: Optional[str] = Field(None, max_length=200)
    tags: Optional[str] = None
    keywords: Optional[str] = None
    is_active: Optional[bool] = None

# 数据库中的政策模式
class PolicyInDB(PolicyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的政策模式
class Policy(PolicyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 政策列表查询参数
class PolicyQuery(BaseModel):
    country: Optional[str] = None
    category: Optional[PolicyCategory] = None
    urgency: Optional[PolicyUrgency] = None
    status: Optional[PolicyStatus] = None
    keyword: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 政策统计模式
class PolicyStats(BaseModel):
    total_policies: int
    by_country: dict
    by_category: dict
    by_urgency: dict
    recent_updates: int
