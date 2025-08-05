from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.compliance_tool import (
    ToolType, ToolCategory, ToolStatus, AccessLevel
)

# 基础合规工具模式
class ComplianceToolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = Field(None, max_length=500)
    tool_type: ToolType
    category: ToolCategory
    status: ToolStatus = ToolStatus.ACTIVE
    access_level: AccessLevel = AccessLevel.FREE
    applicable_regions: Optional[str] = None
    applicable_industries: Optional[str] = None
    applicable_products: Optional[str] = None
    features: Optional[str] = None
    input_requirements: Optional[str] = None
    output_format: Optional[str] = None
    usage_guide: Optional[str] = None
    examples: Optional[str] = None
    faq: Optional[str] = None
    api_endpoint: Optional[str] = Field(None, max_length=500)
    documentation_url: Optional[str] = Field(None, max_length=500)
    source_code_url: Optional[str] = Field(None, max_length=500)
    version: str = Field(default="1.0.0", max_length=50)
    last_updated: Optional[datetime] = None
    changelog: Optional[str] = None
    dependencies: Optional[str] = None
    system_requirements: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    tags: Optional[str] = None
    keywords: Optional[str] = None
    price: float = Field(default=0.0, ge=0.0)
    pricing_model: Optional[str] = Field(None, max_length=100)
    trial_available: bool = False
    vendor: Optional[str] = Field(None, max_length=200)
    contact_email: Optional[str] = Field(None, max_length=100)
    support_url: Optional[str] = Field(None, max_length=500)
    compliance_standards: Optional[str] = None
    regulatory_updates: Optional[str] = None
    audit_trail: bool = False
    is_featured: bool = False
    is_verified: bool = False
    is_popular: bool = False

# 合规工具创建模式
class ComplianceToolCreate(ComplianceToolBase):
    pass

# 合规工具更新模式
class ComplianceToolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = Field(None, max_length=500)
    tool_type: Optional[ToolType] = None
    category: Optional[ToolCategory] = None
    status: Optional[ToolStatus] = None
    access_level: Optional[AccessLevel] = None
    applicable_regions: Optional[str] = None
    applicable_industries: Optional[str] = None
    applicable_products: Optional[str] = None
    features: Optional[str] = None
    input_requirements: Optional[str] = None
    output_format: Optional[str] = None
    usage_guide: Optional[str] = None
    examples: Optional[str] = None
    faq: Optional[str] = None
    api_endpoint: Optional[str] = Field(None, max_length=500)
    documentation_url: Optional[str] = Field(None, max_length=500)
    source_code_url: Optional[str] = Field(None, max_length=500)
    version: Optional[str] = Field(None, max_length=50)
    last_updated: Optional[datetime] = None
    changelog: Optional[str] = None
    dependencies: Optional[str] = None
    system_requirements: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    tags: Optional[str] = None
    keywords: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)
    pricing_model: Optional[str] = Field(None, max_length=100)
    trial_available: Optional[bool] = None
    vendor: Optional[str] = Field(None, max_length=200)
    contact_email: Optional[str] = Field(None, max_length=100)
    support_url: Optional[str] = Field(None, max_length=500)
    compliance_standards: Optional[str] = None
    regulatory_updates: Optional[str] = None
    audit_trail: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_popular: Optional[bool] = None

# 数据库中的合规工具模式
class ComplianceToolInDB(ComplianceToolBase):
    id: int
    usage_count: int
    download_count: int
    review_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的合规工具模式
class ComplianceTool(ComplianceToolBase):
    id: int
    usage_count: int
    download_count: int
    review_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 合规工具列表查询参数
class ComplianceToolQuery(BaseModel):
    tool_type: Optional[ToolType] = None
    category: Optional[ToolCategory] = None
    status: Optional[ToolStatus] = None
    access_level: Optional[AccessLevel] = None
    keyword: Optional[str] = None
    vendor: Optional[str] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_popular: Optional[bool] = None
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    max_price: Optional[float] = Field(None, ge=0.0)
    trial_available: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 合规工具统计模式
class ComplianceToolStats(BaseModel):
    total_tools: int
    by_type: dict
    by_category: dict
    by_access_level: dict
    by_status: dict
    featured_count: int
    verified_count: int
    popular_count: int
    total_usage: int
    avg_rating: float

# 合规工具简要信息（用于列表显示）
class ComplianceToolSummary(BaseModel):
    id: int
    name: str
    short_description: Optional[str]
    tool_type: ToolType
    category: ToolCategory
    access_level: AccessLevel
    rating: float
    usage_count: int
    price: float
    is_featured: bool
    is_verified: bool
    is_popular: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 工具使用日志模式
class ToolUsageLogBase(BaseModel):
    tool_id: int
    input_data: Optional[str] = None
    execution_time: Optional[float] = None

class ToolUsageLogCreate(ToolUsageLogBase):
    session_id: Optional[str] = None

class ToolUsageLog(ToolUsageLogBase):
    id: int
    user_id: Optional[int]
    success: bool
    error_message: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 工具评价模式
class ToolReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)
    ease_of_use: Optional[int] = Field(None, ge=1, le=5)
    accuracy: Optional[int] = Field(None, ge=1, le=5)
    performance: Optional[int] = Field(None, ge=1, le=5)
    support: Optional[int] = Field(None, ge=1, le=5)
    would_recommend: Optional[bool] = None
    use_case: Optional[str] = Field(None, max_length=200)

class ToolReviewCreate(ToolReviewBase):
    tool_id: int

class ToolReview(ToolReviewBase):
    id: int
    tool_id: int
    user_id: Optional[int]
    is_verified: bool
    is_helpful: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 合规法规模式
class ComplianceRegulationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    regulation_code: Optional[str] = Field(None, max_length=100)
    description: str = Field(..., min_length=1)
    category: ToolCategory
    jurisdiction: str = Field(..., min_length=1, max_length=100)
    authority: Optional[str] = Field(None, max_length=200)
    full_text: Optional[str] = None
    summary: Optional[str] = None
    key_requirements: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    last_amended: Optional[datetime] = None
    applicable_entities: Optional[str] = None
    exemptions: Optional[str] = None
    related_regulations: Optional[str] = None
    superseded_by: Optional[int] = None
    official_url: Optional[str] = Field(None, max_length=500)
    guidance_documents: Optional[str] = None
    is_active: bool = True

class ComplianceRegulationCreate(ComplianceRegulationBase):
    pass

class ComplianceRegulationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    regulation_code: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[ToolCategory] = None
    jurisdiction: Optional[str] = Field(None, min_length=1, max_length=100)
    authority: Optional[str] = Field(None, max_length=200)
    full_text: Optional[str] = None
    summary: Optional[str] = None
    key_requirements: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    last_amended: Optional[datetime] = None
    applicable_entities: Optional[str] = None
    exemptions: Optional[str] = None
    related_regulations: Optional[str] = None
    superseded_by: Optional[int] = None
    official_url: Optional[str] = Field(None, max_length=500)
    guidance_documents: Optional[str] = None
    is_active: Optional[bool] = None

class ComplianceRegulation(ComplianceRegulationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
