from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum, JSON
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
import enum

class ToolType(enum.Enum):
    REGULATION_CHECKER = "regulation_checker"     # 法规检查器
    DOCUMENT_TEMPLATE = "document_template"       # 文档模板
    COMPLIANCE_AUDIT = "compliance_audit"         # 合规审计
    RISK_ASSESSMENT = "risk_assessment"           # 风险评估
    CERTIFICATION_GUIDE = "certification_guide"   # 认证指南
    EXPORT_CONTROL = "export_control"             # 出口管制
    TARIFF_CALCULATOR = "tariff_calculator"       # 关税计算器
    LEGAL_DATABASE = "legal_database"             # 法律数据库

class ToolCategory(enum.Enum):
    TRADE_COMPLIANCE = "trade_compliance"         # 贸易合规
    PRODUCT_SAFETY = "product_safety"            # 产品安全
    ENVIRONMENTAL = "environmental"               # 环境合规
    DATA_PRIVACY = "data_privacy"                 # 数据隐私
    FINANCIAL = "financial"                       # 财务合规
    LABOR_LAW = "labor_law"                      # 劳动法
    INTELLECTUAL_PROPERTY = "intellectual_property" # 知识产权
    CUSTOMS = "customs"                          # 海关合规

class ToolStatus(enum.Enum):
    ACTIVE = "active"           # 活跃
    MAINTENANCE = "maintenance" # 维护中
    DEPRECATED = "deprecated"   # 已弃用
    BETA = "beta"              # 测试版

class AccessLevel(enum.Enum):
    FREE = "free"               # 免费
    PREMIUM = "premium"         # 付费
    ENTERPRISE = "enterprise"   # 企业版

class ComplianceTool(Base):
    __tablename__ = "compliance_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    
    # 分类信息
    tool_type = Column(Enum(ToolType), nullable=False, index=True)
    category = Column(Enum(ToolCategory), nullable=False, index=True)
    status = Column(Enum(ToolStatus), default=ToolStatus.ACTIVE, index=True)
    access_level = Column(Enum(AccessLevel), default=AccessLevel.FREE, index=True)
    
    # 适用范围
    applicable_regions = Column(Text, nullable=True)  # JSON格式存储适用地区
    applicable_industries = Column(Text, nullable=True)  # JSON格式存储适用行业
    applicable_products = Column(Text, nullable=True)   # JSON格式存储适用产品
    
    # 功能特性
    features = Column(Text, nullable=True)  # JSON格式存储功能列表
    input_requirements = Column(Text, nullable=True)  # 输入要求
    output_format = Column(Text, nullable=True)       # 输出格式
    
    # 使用指南
    usage_guide = Column(Text, nullable=True)         # 使用指南
    examples = Column(Text, nullable=True)            # 使用示例
    faq = Column(Text, nullable=True)                 # 常见问题
    
    # 技术信息
    api_endpoint = Column(String(500), nullable=True)  # API端点
    documentation_url = Column(String(500), nullable=True)  # 文档链接
    source_code_url = Column(String(500), nullable=True)    # 源码链接
    
    # 版本信息
    version = Column(String(50), default="1.0.0")
    last_updated = Column(DateTime(timezone=True), nullable=True)
    changelog = Column(Text, nullable=True)  # 更新日志
    
    # 依赖和要求
    dependencies = Column(Text, nullable=True)  # JSON格式存储依赖
    system_requirements = Column(Text, nullable=True)  # 系统要求
    
    # 评价和统计
    rating = Column(Float, default=0.0)  # 用户评分 0-5
    usage_count = Column(Integer, default=0)  # 使用次数
    download_count = Column(Integer, default=0)  # 下载次数
    review_count = Column(Integer, default=0)  # 评价数量
    
    # 标签和关键词
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    keywords = Column(Text, nullable=True)  # 搜索关键词
    
    # 价格信息
    price = Column(Float, default=0.0)  # 价格（美元）
    pricing_model = Column(String(100), nullable=True)  # 定价模式
    trial_available = Column(Boolean, default=False)  # 是否提供试用
    
    # 联系信息
    vendor = Column(String(200), nullable=True)  # 供应商
    contact_email = Column(String(100), nullable=True)  # 联系邮箱
    support_url = Column(String(500), nullable=True)  # 支持链接
    
    # 合规相关
    compliance_standards = Column(Text, nullable=True)  # JSON格式存储合规标准
    regulatory_updates = Column(Text, nullable=True)    # 法规更新信息
    audit_trail = Column(Boolean, default=False)       # 是否支持审计跟踪
    
    # 状态标记
    is_featured = Column(Boolean, default=False)  # 是否推荐
    is_verified = Column(Boolean, default=False)  # 是否已验证
    is_popular = Column(Boolean, default=False)   # 是否热门
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)  # 创建者用户ID
    
    def __repr__(self):
        return f"<ComplianceTool(id={self.id}, name='{self.name}', type='{self.tool_type}')>"

class ToolUsageLog(Base):
    __tablename__ = "tool_usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    
    # 使用信息
    session_id = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # 使用详情
    input_data = Column(Text, nullable=True)  # 输入数据
    output_data = Column(Text, nullable=True)  # 输出数据
    execution_time = Column(Float, nullable=True)  # 执行时间（秒）
    success = Column(Boolean, default=True)  # 是否成功
    error_message = Column(Text, nullable=True)  # 错误信息
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ToolUsageLog(id={self.id}, tool_id={self.tool_id})>"

class ToolReview(Base):
    __tablename__ = "tool_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    
    # 评价信息
    rating = Column(Integer, nullable=False)  # 评分 1-5
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    
    # 详细评分
    ease_of_use = Column(Integer, nullable=True)  # 易用性 1-5
    accuracy = Column(Integer, nullable=True)     # 准确性 1-5
    performance = Column(Integer, nullable=True)  # 性能 1-5
    support = Column(Integer, nullable=True)      # 支持 1-5
    
    # 推荐信息
    would_recommend = Column(Boolean, nullable=True)
    use_case = Column(String(200), nullable=True)  # 使用场景
    
    # 状态
    is_verified = Column(Boolean, default=False)  # 是否已验证
    is_helpful = Column(Integer, default=0)       # 有用投票数
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ToolReview(id={self.id}, tool_id={self.tool_id}, rating={self.rating})>"

class ComplianceRegulation(Base):
    __tablename__ = "compliance_regulations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(300), nullable=False, index=True)
    regulation_code = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=False)
    
    # 分类信息
    category = Column(Enum(ToolCategory), nullable=False, index=True)
    jurisdiction = Column(String(100), nullable=False, index=True)  # 管辖区域
    authority = Column(String(200), nullable=True)  # 监管机构
    
    # 内容信息
    full_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    key_requirements = Column(Text, nullable=True)  # JSON格式
    
    # 时间信息
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    last_amended = Column(DateTime(timezone=True), nullable=True)
    
    # 适用范围
    applicable_entities = Column(Text, nullable=True)  # 适用实体
    exemptions = Column(Text, nullable=True)           # 豁免条件
    
    # 关联信息
    related_regulations = Column(Text, nullable=True)  # JSON格式存储相关法规
    superseded_by = Column(Integer, nullable=True)     # 被哪个法规取代
    
    # 链接和资源
    official_url = Column(String(500), nullable=True)
    guidance_documents = Column(Text, nullable=True)  # JSON格式
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ComplianceRegulation(id={self.id}, title='{self.title}')>"
