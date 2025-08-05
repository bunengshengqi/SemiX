from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class ListingType(enum.Enum):
    SELL = "sell"        # 出售
    BUY = "buy"          # 求购
    EXCHANGE = "exchange" # 交换

class ListingStatus(enum.Enum):
    ACTIVE = "active"       # 活跃
    SOLD = "sold"          # 已售出
    EXPIRED = "expired"     # 已过期
    SUSPENDED = "suspended" # 已暂停
    DELETED = "deleted"     # 已删除

class ProductCondition(enum.Enum):
    NEW = "new"                    # 全新
    LIKE_NEW = "like_new"         # 几乎全新
    EXCELLENT = "excellent"        # 优秀
    GOOD = "good"                 # 良好
    FAIR = "fair"                 # 一般
    POOR = "poor"                 # 较差
    FOR_PARTS = "for_parts"       # 仅供配件

class PriceType(enum.Enum):
    FIXED = "fixed"           # 固定价格
    NEGOTIABLE = "negotiable" # 可议价
    AUCTION = "auction"       # 拍卖
    FREE = "free"            # 免费

class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=False)
    listing_type = Column(Enum(ListingType), nullable=False, index=True)
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE, index=True)
    
    # 产品信息
    product_name = Column(String(200), nullable=False, index=True)
    manufacturer = Column(String(100), nullable=True, index=True)
    model_number = Column(String(100), nullable=True, index=True)
    part_number = Column(String(100), nullable=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    
    # 规格参数
    specifications = Column(Text, nullable=True)  # JSON格式存储技术规格
    datasheet_url = Column(String(500), nullable=True)
    
    # 数量和条件
    quantity = Column(Integer, nullable=False, default=1)
    min_order_quantity = Column(Integer, nullable=True)
    condition = Column(Enum(ProductCondition), nullable=False, index=True)
    condition_notes = Column(Text, nullable=True)
    
    # 价格信息
    price = Column(Float, nullable=True)  # 单价
    currency = Column(String(10), default="USD")
    price_type = Column(Enum(PriceType), default=PriceType.FIXED)
    total_value = Column(Float, nullable=True)  # 总价值
    
    # 地理信息
    country = Column(String(100), nullable=False, index=True)
    state_province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    shipping_from = Column(String(200), nullable=True)
    
    # 交易条件
    payment_terms = Column(String(200), nullable=True)
    shipping_terms = Column(String(200), nullable=True)
    delivery_time = Column(String(100), nullable=True)
    warranty_info = Column(String(200), nullable=True)
    
    # 联系信息
    contact_name = Column(String(100), nullable=True)
    contact_email = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    company_name = Column(String(200), nullable=True)
    
    # 图片和文档
    images = Column(Text, nullable=True)  # JSON格式存储图片URL列表
    documents = Column(Text, nullable=True)  # JSON格式存储文档URL列表
    
    # 时间信息
    expires_at = Column(DateTime(timezone=True), nullable=True)
    sold_at = Column(DateTime(timezone=True), nullable=True)
    
    # 统计信息
    view_count = Column(Integer, default=0)
    inquiry_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    
    # 标签和关键词
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    keywords = Column(Text, nullable=True)
    
    # 验证和推荐
    is_verified = Column(Boolean, default=False)  # 是否已验证
    is_featured = Column(Boolean, default=False)  # 是否推荐
    is_urgent = Column(Boolean, default=False)    # 是否紧急
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    creator = relationship("User", back_populates="marketplace_listings")
    inquiries = relationship("MarketplaceInquiry", back_populates="listing")
    favorites = relationship("MarketplaceFavorite", back_populates="listing")
    
    def __repr__(self):
        return f"<MarketplaceListing(id={self.id}, title='{self.title}', type='{self.listing_type}')>"

class MarketplaceInquiry(Base):
    __tablename__ = "marketplace_inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace_listings.id"), nullable=False, index=True)
    
    # 询价信息
    inquirer_name = Column(String(100), nullable=False)
    inquirer_email = Column(String(100), nullable=False)
    inquirer_phone = Column(String(50), nullable=True)
    inquirer_company = Column(String(200), nullable=True)
    
    # 询价内容
    message = Column(Text, nullable=False)
    requested_quantity = Column(Integer, nullable=True)
    target_price = Column(Float, nullable=True)
    urgency = Column(String(50), nullable=True)  # 紧急程度
    
    # 状态
    status = Column(String(50), default="pending")  # pending, replied, closed
    reply_message = Column(Text, nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    listing = relationship("MarketplaceListing", back_populates="inquiries")
    inquirer = relationship("User")
    
    def __repr__(self):
        return f"<MarketplaceInquiry(id={self.id}, listing_id={self.listing_id})>"

class MarketplaceFavorite(Base):
    __tablename__ = "marketplace_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace_listings.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    listing = relationship("MarketplaceListing", back_populates="favorites")
    user = relationship("User")
    
    def __repr__(self):
        return f"<MarketplaceFavorite(id={self.id}, listing_id={self.listing_id}, user_id={self.user_id})>"

class MarketplaceCategory(Base):
    __tablename__ = "marketplace_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    name_en = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("marketplace_categories.id"), nullable=True)
    
    # 显示信息
    icon = Column(String(100), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # 统计信息
    listing_count = Column(Integer, default=0)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    parent = relationship("MarketplaceCategory", remote_side=[id])
    children = relationship("MarketplaceCategory")
    
    def __repr__(self):
        return f"<MarketplaceCategory(id={self.id}, name='{self.name}')>"

class MarketplaceReport(Base):
    __tablename__ = "marketplace_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace_listings.id"), nullable=False, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 举报信息
    reason = Column(String(100), nullable=False)  # 举报原因
    description = Column(Text, nullable=True)
    evidence_urls = Column(Text, nullable=True)  # JSON格式存储证据链接
    
    # 处理状态
    status = Column(String(50), default="pending")  # pending, reviewing, resolved, dismissed
    admin_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    listing = relationship("MarketplaceListing")
    reporter = relationship("User", foreign_keys=[reporter_id])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<MarketplaceReport(id={self.id}, listing_id={self.listing_id}, reason='{self.reason}')>"
