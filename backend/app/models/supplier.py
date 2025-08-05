from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
import enum

class SupplierType(enum.Enum):
    MANUFACTURER = "manufacturer"  # 制造商
    DISTRIBUTOR = "distributor"    # 分销商
    TRADER = "trader"              # 贸易商
    SERVICE_PROVIDER = "service_provider"  # 服务商

class SupplierScale(enum.Enum):
    LARGE = "large"        # 大型企业
    MEDIUM = "medium"      # 中型企业
    SMALL = "small"        # 小型企业
    STARTUP = "startup"    # 初创企业

class CertificationLevel(enum.Enum):
    PREMIUM = "premium"    # 金牌认证
    VERIFIED = "verified"  # 认证供应商
    BASIC = "basic"        # 基础认证
    UNVERIFIED = "unverified"  # 未认证

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    company_name = Column(String(200), nullable=False, index=True)
    company_name_en = Column(String(200), nullable=True)
    brand_name = Column(String(100), nullable=True)
    
    # 联系信息
    contact_person = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(200), nullable=True)
    
    # 地址信息
    country = Column(String(50), nullable=False, index=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    # 企业信息
    supplier_type = Column(Enum(SupplierType), nullable=False, index=True)
    scale = Column(Enum(SupplierScale), nullable=False, index=True)
    established_year = Column(Integer, nullable=True)
    employee_count = Column(Integer, nullable=True)
    annual_revenue = Column(Float, nullable=True)  # 年营收（万美元）
    
    # 产品和服务
    main_products = Column(Text, nullable=False)  # JSON格式存储
    product_categories = Column(Text, nullable=False)  # JSON格式存储
    service_scope = Column(Text, nullable=True)  # 服务范围
    
    # 技术能力
    technology_level = Column(String(50), nullable=True)  # 技术水平
    certifications = Column(Text, nullable=True)  # JSON格式存储认证信息
    patents_count = Column(Integer, default=0)
    
    # 质量和认证
    certification_level = Column(Enum(CertificationLevel), default=CertificationLevel.UNVERIFIED, index=True)
    quality_certifications = Column(Text, nullable=True)  # ISO等质量认证
    
    # 评级信息
    overall_rating = Column(Float, default=0.0)  # 综合评分 0-5
    quality_rating = Column(Float, default=0.0)  # 质量评分
    service_rating = Column(Float, default=0.0)  # 服务评分
    delivery_rating = Column(Float, default=0.0)  # 交付评分
    price_rating = Column(Float, default=0.0)    # 价格评分
    review_count = Column(Integer, default=0)    # 评价数量
    
    # 业务信息
    min_order_quantity = Column(String(50), nullable=True)  # 最小起订量
    payment_terms = Column(String(100), nullable=True)      # 付款条件
    delivery_time = Column(String(50), nullable=True)       # 交付周期
    export_countries = Column(Text, nullable=True)          # 出口国家列表
    
    # 合作信息
    major_clients = Column(Text, nullable=True)  # 主要客户
    partnerships = Column(Text, nullable=True)   # 合作伙伴
    
    # 展会和活动
    exhibitions = Column(Text, nullable=True)    # 参展信息
    awards = Column(Text, nullable=True)         # 获奖信息
    
    # 描述信息
    company_description = Column(Text, nullable=True)
    competitive_advantages = Column(Text, nullable=True)  # 竞争优势
    
    # 标签和关键词
    tags = Column(Text, nullable=True)     # JSON格式存储标签
    keywords = Column(Text, nullable=True) # 搜索关键词
    
    # 状态信息
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # 是否推荐
    is_verified = Column(Boolean, default=False)  # 是否已验证
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)  # 创建者用户ID
    
    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.company_name}', country='{self.country}')>"
