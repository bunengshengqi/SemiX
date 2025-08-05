from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.community import (
    PostType, PostStatus, PostPriority
)

# 基础帖子模式
class CommunityPostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    post_type: PostType
    priority: PostPriority = PostPriority.NORMAL
    category_id: Optional[int] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    images: Optional[str] = None
    attachments: Optional[str] = None
    external_links: Optional[str] = None

# 创建帖子模式
class CommunityPostCreate(CommunityPostBase):
    pass

# 更新帖子模式
class CommunityPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    post_type: Optional[PostType] = None
    priority: Optional[PostPriority] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    keywords: Optional[str] = None
    images: Optional[str] = None
    attachments: Optional[str] = None
    external_links: Optional[str] = None
    status: Optional[PostStatus] = None
    is_featured: Optional[bool] = None
    is_official: Optional[bool] = None
    is_expert_verified: Optional[bool] = None
    is_solved: Optional[bool] = None

# 数据库中的帖子模式
class CommunityPostInDB(CommunityPostBase):
    id: int
    status: PostStatus
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    share_count: int
    favorite_count: int
    quality_score: float
    helpfulness_score: float
    is_featured: bool
    is_official: bool
    is_expert_verified: bool
    is_hot: bool
    is_urgent: bool
    is_solved: bool
    published_at: Optional[datetime] = None
    last_activity_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    model_config = ConfigDict(from_attributes=True)

# 返回给客户端的帖子模式
class CommunityPost(CommunityPostBase):
    id: int
    status: PostStatus
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    share_count: int
    favorite_count: int
    quality_score: float
    helpfulness_score: float
    is_featured: bool
    is_official: bool
    is_expert_verified: bool
    is_hot: bool
    is_urgent: bool
    is_solved: bool
    published_at: Optional[datetime] = None
    last_activity_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # 作者信息
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# 帖子查询参数
class CommunityPostQuery(BaseModel):
    post_type: Optional[PostType] = None
    status: Optional[PostStatus] = None
    priority: Optional[PostPriority] = None
    category_id: Optional[int] = None
    keyword: Optional[str] = None
    author_id: Optional[int] = None
    is_featured: Optional[bool] = None
    is_official: Optional[bool] = None
    is_expert_verified: Optional[bool] = None
    is_hot: Optional[bool] = None
    is_urgent: Optional[bool] = None
    is_solved: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="last_activity_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

# 社区统计模式
class CommunityStats(BaseModel):
    total_posts: int
    active_posts: int
    by_type: dict
    by_category: dict
    by_priority: dict
    featured_count: int
    official_count: int
    expert_verified_count: int
    hot_count: int
    urgent_count: int
    solved_count: int
    total_views: int
    total_comments: int
    total_likes: int

# 帖子简要信息（用于列表显示）
class CommunityPostSummary(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    post_type: PostType
    priority: PostPriority
    category_name: Optional[str]
    author_name: Optional[str]
    view_count: int
    like_count: int
    comment_count: int
    is_featured: bool
    is_official: bool
    is_expert_verified: bool
    is_hot: bool
    is_urgent: bool
    is_solved: bool
    last_activity_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 评论模式
class CommunityCommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    images: Optional[str] = None

class CommunityCommentCreate(CommunityCommentBase):
    post_id: int
    parent_id: Optional[int] = None

class CommunityCommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    images: Optional[str] = None
    is_best_answer: Optional[bool] = None

class CommunityComment(CommunityCommentBase):
    id: int
    post_id: int
    parent_id: Optional[int]
    like_count: int
    dislike_count: int
    reply_count: int
    is_author_reply: bool
    is_expert_answer: bool
    is_best_answer: bool
    is_official: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    # 作者信息
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# 分类模式
class CommunityCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=20)
    parent_id: Optional[int] = None
    sort_order: int = 0
    is_active: bool = True
    is_featured: bool = False
    min_level_to_post: int = 0

class CommunityCategoryCreate(CommunityCategoryBase):
    pass

class CommunityCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=20)
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    min_level_to_post: Optional[int] = None

class CommunityCategory(CommunityCategoryBase):
    id: int
    post_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# 点赞模式
class CommunityLikeCreate(BaseModel):
    post_id: int
    is_like: bool = True

class CommunityLike(BaseModel):
    id: int
    post_id: int
    user_id: int
    is_like: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 评论点赞模式
class CommunityCommentLikeCreate(BaseModel):
    comment_id: int
    is_like: bool = True

class CommunityCommentLike(BaseModel):
    id: int
    comment_id: int
    user_id: int
    is_like: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 收藏模式
class CommunityFavoriteCreate(BaseModel):
    post_id: int
    folder_name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None

class CommunityFavorite(BaseModel):
    id: int
    post_id: int
    user_id: int
    folder_name: Optional[str]
    notes: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 举报模式
class CommunityReportCreate(BaseModel):
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    reported_user_id: int
    reason: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    evidence_urls: Optional[str] = None

class CommunityReport(BaseModel):
    id: int
    post_id: Optional[int]
    comment_id: Optional[int]
    reported_user_id: int
    reporter_id: int
    reason: str
    description: Optional[str]
    status: str
    admin_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 专家模式
class CommunityExpertBase(BaseModel):
    expertise_areas: str = Field(..., min_length=1)
    certification_level: str = Field(default="verified")
    bio: Optional[str] = None
    achievements: Optional[str] = None

class CommunityExpertCreate(CommunityExpertBase):
    user_id: int

class CommunityExpertUpdate(BaseModel):
    expertise_areas: Optional[str] = Field(None, min_length=1)
    certification_level: Optional[str] = None
    bio: Optional[str] = None
    achievements: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None

class CommunityExpert(CommunityExpertBase):
    id: int
    user_id: int
    answer_count: int
    best_answer_count: int
    helpful_votes: int
    reputation_score: float
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # 用户信息
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
