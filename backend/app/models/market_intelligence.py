from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
import enum

class IntelligenceType(enum.Enum):
    MARKET_TREND = "market_trend"           # 市场趋势
    PRICE_ANALYSIS = "price_analysis"       # 价格分析
    SUPPLY_CHAIN = "supply_chain"           # 供应链情报
    TECHNOLOGY_TREND = "technology_trend"   # 技术趋势
    COMPETITOR_ANALYSIS = "competitor_analysis"  # 竞争对手分析
    INDUSTRY_NEWS = "industry_news"         # 行业新闻
    POLICY_IMPACT = "policy_impact"         # 政策影响
    FINANCIAL_REPORT = "financial_report"   # 财务报告

class IntelligencePriority(enum.Enum):
    CRITICAL = "critical"    # 紧急
    HIGH = "high"           # 高
    MEDIUM = "medium"       # 中
    LOW = "low"            # 低

class IntelligenceStatus(enum.Enum):
    DRAFT = "draft"         # 草稿
    PUBLISHED = "published" # 已发布
    ARCHIVED = "archived"   # 已归档
    FEATURED = "featured"   # 精选

class MarketRegion(enum.Enum):
    GLOBAL = "global"           # 全球
    ASIA_PACIFIC = "asia_pacific"  # 亚太
    NORTH_AMERICA = "north_america"  # 北美
    EUROPE = "europe"           # 欧洲
    CHINA = "china"             # 中国
    JAPAN = "japan"             # 日本
    SOUTH_KOREA = "south_korea" # 韩国
    TAIWAN = "taiwan"           # 台湾省
    SOUTHEAST_ASIA = "southeast_asia"  # 东南亚

class MarketIntelligence(Base):
    __tablename__ = "market_intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(300), nullable=False, index=True)
    subtitle = Column(String(500), nullable=True)
    summary = Column(Text, nullable=False)  # 摘要
    content = Column(Text, nullable=False)  # 详细内容
    
    # 分类信息
    intelligence_type = Column(Enum(IntelligenceType), nullable=False, index=True)
    priority = Column(Enum(IntelligencePriority), default=IntelligencePriority.MEDIUM, index=True)
    status = Column(Enum(IntelligenceStatus), default=IntelligenceStatus.DRAFT, index=True)
    
    # 地区和行业
    region = Column(Enum(MarketRegion), default=MarketRegion.GLOBAL, index=True)
    industry_sectors = Column(Text, nullable=True)  # JSON格式存储行业领域
    product_categories = Column(Text, nullable=True)  # JSON格式存储产品类别
    
    # 关键指标
    market_size = Column(Float, nullable=True)  # 市场规模（亿美元）
    growth_rate = Column(Float, nullable=True)  # 增长率（%）
    market_share = Column(Float, nullable=True)  # 市场份额（%）
    price_change = Column(Float, nullable=True)  # 价格变化（%）
    
    # 时间相关
    report_date = Column(DateTime(timezone=True), nullable=False)  # 报告日期
    data_period_start = Column(DateTime(timezone=True), nullable=True)  # 数据周期开始
    data_period_end = Column(DateTime(timezone=True), nullable=True)    # 数据周期结束
    
    # 来源信息
    data_sources = Column(Text, nullable=True)  # JSON格式存储数据来源
    author = Column(String(100), nullable=True)  # 作者
    organization = Column(String(200), nullable=True)  # 发布机构
    
    # 标签和关键词
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    keywords = Column(Text, nullable=True)  # 搜索关键词
    
    # 附件和链接
    attachments = Column(Text, nullable=True)  # JSON格式存储附件信息
    external_links = Column(Text, nullable=True)  # JSON格式存储外部链接
    
    # 互动数据
    view_count = Column(Integer, default=0)  # 浏览次数
    like_count = Column(Integer, default=0)  # 点赞数
    share_count = Column(Integer, default=0)  # 分享数
    comment_count = Column(Integer, default=0)  # 评论数
    
    # 评分和推荐
    quality_score = Column(Float, default=0.0)  # 质量评分 0-5
    relevance_score = Column(Float, default=0.0)  # 相关性评分 0-5
    timeliness_score = Column(Float, default=0.0)  # 时效性评分 0-5
    
    # 状态标记
    is_featured = Column(Boolean, default=False)  # 是否精选
    is_trending = Column(Boolean, default=False)  # 是否热门
    is_premium = Column(Boolean, default=False)   # 是否付费内容
    is_verified = Column(Boolean, default=False)  # 是否已验证
    
    # 访问控制
    access_level = Column(String(50), default="public")  # public, member, premium
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, nullable=True)  # 创建者用户ID
    
    def __repr__(self):
        return f"<MarketIntelligence(id={self.id}, title='{self.title}', type='{self.intelligence_type}')>"

class IntelligenceComment(Base):
    __tablename__ = "intelligence_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    intelligence_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    author_name = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, nullable=True)  # 回复的评论ID
    
    # 状态
    is_approved = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<IntelligenceComment(id={self.id}, intelligence_id={self.intelligence_id})>"

class IntelligenceView(Base):
    __tablename__ = "intelligence_views"
    
    id = Column(Integer, primary_key=True, index=True)
    intelligence_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    view_duration = Column(Integer, nullable=True)  # 浏览时长（秒）
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<IntelligenceView(id={self.id}, intelligence_id={self.intelligence_id})>"
