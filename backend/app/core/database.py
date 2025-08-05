from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 如果没有配置数据库URL，使用SQLite作为默认数据库
DATABASE_URL = settings.DATABASE_URL or "sqlite:///./semix.db"

# 创建数据库引擎
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建所有表
def create_tables():
    from app.models.user import User  # 导入所有模型
    from app.models.policy import Policy
    from app.models.supplier import Supplier
    from app.models.market_intelligence import MarketIntelligence, IntelligenceComment, IntelligenceView
    from app.models.compliance_tool import ComplianceTool, ToolUsageLog, ToolReview, ComplianceRegulation
    from app.models.marketplace import MarketplaceListing, MarketplaceInquiry, MarketplaceFavorite, MarketplaceCategory, MarketplaceReport
    from app.models.community import CommunityPost, CommunityComment, CommunityLike, CommunityCommentLike, CommunityFavorite, CommunityCategory, CommunityReport, CommunityExpert
    Base.metadata.create_all(bind=engine)
