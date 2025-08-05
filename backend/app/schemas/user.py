from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

# 基础用户模式
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    user_type: str = Field(default="individual", pattern="^(individual|company)$")
    industry: Optional[str] = None
    position: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = True

# 用户创建模式
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
    
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("密码和确认密码不匹配")
        return self

# 用户更新模式
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    position: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    bio: Optional[str] = None

# 用户登录模式
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 数据库中的用户模式
class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_verified: bool = False
    is_superuser: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的用户模式
class User(UserBase):
    id: int
    is_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Token相关模式
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
