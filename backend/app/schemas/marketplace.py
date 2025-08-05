from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.marketplace import (
    ListingType, ListingStatus, ProductCondition, PriceType
)

# 基础交易信息模式
class MarketplaceListingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: str = Field(..., min_length=1)
    listing_type: ListingType
    product_name: str = Field(..., min_length=1, max_length=200)
    manufacturer: Optional[str] = Field(None, max_length=100)
    model_number: Optional[str] = Field(None, max_length=100)
    part_number: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    specifications: Optional[str] = None
    datasheet_url: Optional[str] = Field(None, max_length=500)
    quantity: int = Field(..., ge=1)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    condition: ProductCondition
    condition_notes: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=10)
    price_type: PriceType = PriceType.FIXED
    total_value: Optional[float] = Field(None, ge=0)
    country: str = Field(..., min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    shipping_from: Optional[str] = Field(None, max_length=200)
    payment_terms: Optional[str] = Field(None, max_length=200)
    shipping_terms: Optional[str] = Field(None, max_length=200)
    delivery_time: Optional[str] = Field(None, max_length=100)
    warranty_info: Optional[str] = Field(None, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=50)
    company_name: Optional[str] = Field(None, max_length=200)
    images: Optional[str] = None
    documents: Optional[str] = None
    expires_at: Optional[datetime] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    is_urgent: bool = False

# 创建交易信息模式
class MarketplaceListingCreate(MarketplaceListingBase):
    pass

# 更新交易信息模式
class MarketplaceListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = Field(None, min_length=1)
    listing_type: Optional[ListingType] = None
    product_name: Optional[str] = Field(None, min_length=1, max_length=200)
    manufacturer: Optional[str] = Field(None, max_length=100)
    model_number: Optional[str] = Field(None, max_length=100)
    part_number: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    specifications: Optional[str] = None
    datasheet_url: Optional[str] = Field(None, max_length=500)
    quantity: Optional[int] = Field(None, ge=1)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    condition: Optional[ProductCondition] = None
    condition_notes: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    price_type: Optional[PriceType] = None
    total_value: Optional[float] = Field(None, ge=0)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    shipping_from: Optional[str] = Field(None, max_length=200)
    payment_terms: Optional[str] = Field(None, max_length=200)
    shipping_terms: Optional[str] = Field(None, max_length=200)
    delivery_time: Optional[str] = Field(None, max_length=100)
    warranty_info: Optional[str] = Field(None, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=50)
    company_name: Optional[str] = Field(None, max_length=200)
    images: Optional[str] = None
    documents: Optional[str] = None
    expires_at: Optional[datetime] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    is_urgent: Optional[bool] = None
    status: Optional[ListingStatus] = None

# 数据库中的交易信息模式
class MarketplaceListingInDB(MarketplaceListingBase):
    id: int
    status: ListingStatus
    view_count: int
    inquiry_count: int
    favorite_count: int
    is_verified: bool
    is_featured: bool
    sold_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的交易信息模式
class MarketplaceListing(MarketplaceListingBase):
    id: int
    status: ListingStatus
    view_count: int
    inquiry_count: int
    favorite_count: int
    is_verified: bool
    is_featured: bool
    sold_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 交易信息查询参数
class MarketplaceListingQuery(BaseModel):
    listing_type: Optional[ListingType] = None
    status: Optional[ListingStatus] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    condition: Optional[ProductCondition] = None
    price_type: Optional[PriceType] = None
    country: Optional[str] = None
    keyword: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_verified: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_urgent: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 交易统计模式
class MarketplaceStats(BaseModel):
    total_listings: int
    active_listings: int
    by_type: dict
    by_category: dict
    by_condition: dict
    by_country: dict
    featured_count: int
    verified_count: int
    urgent_count: int
    total_views: int
    total_inquiries: int

# 交易简要信息（用于列表显示）
class MarketplaceListingSummary(BaseModel):
    id: int
    title: str
    listing_type: ListingType
    product_name: str
    manufacturer: Optional[str]
    condition: ProductCondition
    price: Optional[float]
    currency: str
    price_type: PriceType
    quantity: int
    country: str
    city: Optional[str]
    is_verified: bool
    is_featured: bool
    is_urgent: bool
    view_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 询价信息模式
class MarketplaceInquiryBase(BaseModel):
    inquirer_name: str = Field(..., min_length=1, max_length=100)
    inquirer_email: str = Field(..., min_length=1, max_length=100)
    inquirer_phone: Optional[str] = Field(None, max_length=50)
    inquirer_company: Optional[str] = Field(None, max_length=200)
    message: str = Field(..., min_length=1)
    requested_quantity: Optional[int] = Field(None, ge=1)
    target_price: Optional[float] = Field(None, ge=0)
    urgency: Optional[str] = Field(None, max_length=50)

class MarketplaceInquiryCreate(MarketplaceInquiryBase):
    listing_id: int

class MarketplaceInquiry(MarketplaceInquiryBase):
    id: int
    listing_id: int
    status: str
    reply_message: Optional[str]
    replied_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 收藏模式
class MarketplaceFavoriteCreate(BaseModel):
    listing_id: int

class MarketplaceFavorite(BaseModel):
    id: int
    listing_id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 分类模式
class MarketplaceCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = Field(None, max_length=100)
    sort_order: int = 0
    is_active: bool = True

class MarketplaceCategoryCreate(MarketplaceCategoryBase):
    pass

class MarketplaceCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = Field(None, max_length=100)
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class MarketplaceCategory(MarketplaceCategoryBase):
    id: int
    listing_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 举报模式
class MarketplaceReportCreate(BaseModel):
    listing_id: int
    reason: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    evidence_urls: Optional[str] = None

class MarketplaceReport(BaseModel):
    id: int
    listing_id: int
    reporter_id: Optional[int]
    reason: str
    description: Optional[str]
    status: str
    admin_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
