from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SemiX - 半导体出海信息服务平台"

    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 爬虫配置
    USER_AGENT: str = "SemiX-Bot/1.0"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "application/pdf"]
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
