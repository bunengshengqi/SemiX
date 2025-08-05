from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    users,
    policies,
    suppliers,
    market_intelligence,
    compliance_tools,
    community,
    marketplace
)

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 用户管理路由
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 政策监控路由
api_router.include_router(policies.router, prefix="/policies", tags=["政策监控"])

# 供应商目录路由
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["供应商目录"])

# 市场情报路由
api_router.include_router(market_intelligence.router, prefix="/market", tags=["市场情报"])

# 合规工具路由
api_router.include_router(compliance_tools.router, prefix="/compliance", tags=["合规工具"])

# 社区讨论路由
api_router.include_router(community.router, prefix="/community", tags=["社区讨论"])

# 二手交易路由
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["二手交易"])
