from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.database import create_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="半导体出海信息服务平台 - 为半导体企业提供出海全链条信息服务",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 设置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 添加受信任主机中间件
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 暂时注释掉启动事件，先让服务器启动
# @app.on_event("startup")
# async def startup_event():
#     """应用启动时创建数据库表"""
#     try:
#         create_tables()
#         print("✅ 数据库表创建成功")
#     except Exception as e:
#         print(f"❌ 数据库表创建失败: {e}")

@app.get("/")
async def root():
    return {
        "message": "欢迎使用SemiX半导体出海信息服务平台API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SemiX API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
