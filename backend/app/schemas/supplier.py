from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.supplier import SupplierType, SupplierScale, CertificationLevel

# 基础供应商模式
class SupplierBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200)
    company_name_en: Optional[str] = Field(None, max_length=200)
    brand_name: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=200)
    country: str = Field(..., min_length=1, max_length=50)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    supplier_type: SupplierType
    scale: SupplierScale
    established_year: Optional[int] = Field(None, ge=1900, le=2024)
    employee_count: Optional[int] = Field(None, ge=0)
    annual_revenue: Optional[float] = Field(None, ge=0)
    main_products: str = Field(..., min_length=1)
    product_categories: str = Field(..., min_length=1)
    service_scope: Optional[str] = None
    technology_level: Optional[str] = Field(None, max_length=50)
    certifications: Optional[str] = None
    patents_count: int = Field(default=0, ge=0)
    certification_level: CertificationLevel = CertificationLevel.UNVERIFIED
    quality_certifications: Optional[str] = None
    overall_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    quality_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    service_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    delivery_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    price_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    review_count: int = Field(default=0, ge=0)
    min_order_quantity: Optional[str] = Field(None, max_length=50)
    payment_terms: Optional[str] = Field(None, max_length=100)
    delivery_time: Optional[str] = Field(None, max_length=50)
    export_countries: Optional[str] = None
    major_clients: Optional[str] = None
    partnerships: Optional[str] = None
    exhibitions: Optional[str] = None
    awards: Optional[str] = None
    company_description: Optional[str] = None
    competitive_advantages: Optional[str] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    is_active: bool = True
    is_featured: bool = False
    is_verified: bool = False

# 供应商创建模式
class SupplierCreate(SupplierBase):
    pass

# 供应商更新模式
class SupplierUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=200)
    company_name_en: Optional[str] = Field(None, max_length=200)
    brand_name: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=200)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    supplier_type: Optional[SupplierType] = None
    scale: Optional[SupplierScale] = None
    established_year: Optional[int] = Field(None, ge=1900, le=2024)
    employee_count: Optional[int] = Field(None, ge=0)
    annual_revenue: Optional[float] = Field(None, ge=0)
    main_products: Optional[str] = Field(None, min_length=1)
    product_categories: Optional[str] = Field(None, min_length=1)
    service_scope: Optional[str] = None
    technology_level: Optional[str] = Field(None, max_length=50)
    certifications: Optional[str] = None
    patents_count: Optional[int] = Field(None, ge=0)
    certification_level: Optional[CertificationLevel] = None
    quality_certifications: Optional[str] = None
    overall_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    quality_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    service_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    delivery_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    price_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    review_count: Optional[int] = Field(None, ge=0)
    min_order_quantity: Optional[str] = Field(None, max_length=50)
    payment_terms: Optional[str] = Field(None, max_length=100)
    delivery_time: Optional[str] = Field(None, max_length=50)
    export_countries: Optional[str] = None
    major_clients: Optional[str] = None
    partnerships: Optional[str] = None
    exhibitions: Optional[str] = None
    awards: Optional[str] = None
    company_description: Optional[str] = None
    competitive_advantages: Optional[str] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None

# 数据库中的供应商模式
class SupplierInDB(SupplierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的供应商模式
class Supplier(SupplierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 供应商列表查询参数
class SupplierQuery(BaseModel):
    country: Optional[str] = None
    supplier_type: Optional[SupplierType] = None
    scale: Optional[SupplierScale] = None
    certification_level: Optional[CertificationLevel] = None
    product_category: Optional[str] = None
    keyword: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_verified: Optional[bool] = None
    is_featured: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="overall_rating")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 供应商统计模式
class SupplierStats(BaseModel):
    total_suppliers: int
    by_country: dict
    by_type: dict
    by_scale: dict
    by_certification: dict
    verified_count: int
    featured_count: int
    avg_rating: float

# 供应商简要信息（用于列表显示）
class SupplierSummary(BaseModel):
    id: int
    company_name: str
    country: str
    city: Optional[str]
    supplier_type: SupplierType
    certification_level: CertificationLevel
    overall_rating: float
    review_count: int
    main_products: str
    is_verified: bool
    is_featured: bool
    
    model_config = ConfigDict(from_attributes=True)
