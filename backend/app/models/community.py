from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class PostType(enum.Enum):
    DISCUSSION = "discussion"    # 讨论
    QUESTION = "question"       # 问题
    EXPERIENCE = "experience"   # 经验分享
    NEWS = "news"              # 新闻资讯
    POLICY = "policy"          # 政策解读
    TECHNICAL = "technical"    # 技术交流
    MARKET = "market"          # 市场分析
    COOPERATION = "cooperation" # 合作对接

class PostStatus(enum.Enum):
    DRAFT = "draft"           # 草稿
    PUBLISHED = "published"   # 已发布
    HIDDEN = "hidden"         # 已隐藏
    DELETED = "deleted"       # 已删除
    PINNED = "pinned"         # 置顶

class PostPriority(enum.Enum):
    LOW = "low"              # 低优先级
    NORMAL = "normal"        # 普通
    HIGH = "high"            # 高优先级
    URGENT = "urgent"        # 紧急

class CommunityPost(Base):
    __tablename__ = "community_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(300), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)  # 摘要
    post_type = Column(Enum(PostType), nullable=False, index=True)
    status = Column(Enum(PostStatus), default=PostStatus.PUBLISHED, index=True)
    priority = Column(Enum(PostPriority), default=PostPriority.NORMAL, index=True)
    
    # 分类和标签
    category_id = Column(Integer, ForeignKey("community_categories.id"), nullable=True, index=True)
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    keywords = Column(Text, nullable=True)
    
    # 内容相关
    images = Column(Text, nullable=True)  # JSON格式存储图片URL
    attachments = Column(Text, nullable=True)  # JSON格式存储附件URL
    external_links = Column(Text, nullable=True)  # JSON格式存储外部链接
    
    # 互动统计
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    
    # 质量评分
    quality_score = Column(Float, default=0.0)  # 内容质量评分
    helpfulness_score = Column(Float, default=0.0)  # 有用性评分
    
    # 特殊标记
    is_featured = Column(Boolean, default=False)  # 是否推荐
    is_official = Column(Boolean, default=False)  # 是否官方发布
    is_expert_verified = Column(Boolean, default=False)  # 是否专家认证
    is_hot = Column(Boolean, default=False)  # 是否热门
    is_urgent = Column(Boolean, default=False)  # 是否紧急
    is_solved = Column(Boolean, default=False)  # 是否已解决（针对问题类型）
    
    # 时间信息
    published_at = Column(DateTime(timezone=True), nullable=True)
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 关系
    author = relationship("User", back_populates="community_posts")
    category = relationship("CommunityCategory", back_populates="posts")
    comments = relationship("CommunityComment", back_populates="post")
    likes = relationship("CommunityLike", back_populates="post")
    favorites = relationship("CommunityFavorite", back_populates="post")
    
    def __repr__(self):
        return f"<CommunityPost(id={self.id}, title='{self.title}', type='{self.post_type}')>"

class CommunityCategory(Base):
    __tablename__ = "community_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    name_en = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)  # 分类颜色
    
    # 层级结构
    parent_id = Column(Integer, ForeignKey("community_categories.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # 统计信息
    post_count = Column(Integer, default=0)
    
    # 权限设置
    min_level_to_post = Column(Integer, default=0)  # 发帖最低等级要求
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    parent = relationship("CommunityCategory", remote_side=[id])
    children = relationship("CommunityCategory")
    posts = relationship("CommunityPost", back_populates="category")
    
    def __repr__(self):
        return f"<CommunityCategory(id={self.id}, name='{self.name}')>"

class CommunityComment(Base):
    __tablename__ = "community_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("community_comments.id"), nullable=True)  # 回复评论
    
    # 内容
    content = Column(Text, nullable=False)
    images = Column(Text, nullable=True)  # JSON格式存储图片
    
    # 互动统计
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    
    # 特殊标记
    is_author_reply = Column(Boolean, default=False)  # 是否作者回复
    is_expert_answer = Column(Boolean, default=False)  # 是否专家回答
    is_best_answer = Column(Boolean, default=False)  # 是否最佳答案
    is_official = Column(Boolean, default=False)  # 是否官方回复
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    post = relationship("CommunityPost", back_populates="comments")
    author = relationship("User")
    parent = relationship("CommunityComment", remote_side=[id])
    replies = relationship("CommunityComment")
    likes = relationship("CommunityCommentLike", back_populates="comment")
    
    def __repr__(self):
        return f"<CommunityComment(id={self.id}, post_id={self.post_id})>"

class CommunityLike(Base):
    __tablename__ = "community_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_like = Column(Boolean, default=True)  # True=点赞, False=点踩
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    post = relationship("CommunityPost", back_populates="likes")
    user = relationship("User")
    
    def __repr__(self):
        return f"<CommunityLike(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

class CommunityCommentLike(Base):
    __tablename__ = "community_comment_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("community_comments.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_like = Column(Boolean, default=True)  # True=点赞, False=点踩
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    comment = relationship("CommunityComment", back_populates="likes")
    user = relationship("User")
    
    def __repr__(self):
        return f"<CommunityCommentLike(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id})>"

class CommunityFavorite(Base):
    __tablename__ = "community_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 收藏分类
    folder_name = Column(String(100), nullable=True)  # 收藏夹名称
    notes = Column(Text, nullable=True)  # 收藏备注
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    post = relationship("CommunityPost", back_populates="favorites")
    user = relationship("User")
    
    def __repr__(self):
        return f"<CommunityFavorite(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

class CommunityReport(Base):
    __tablename__ = "community_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=True, index=True)
    comment_id = Column(Integer, ForeignKey("community_comments.id"), nullable=True, index=True)
    reported_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 举报信息
    reason = Column(String(100), nullable=False)  # 举报原因
    description = Column(Text, nullable=True)
    evidence_urls = Column(Text, nullable=True)  # JSON格式存储证据
    
    # 处理状态
    status = Column(String(50), default="pending")  # pending, reviewing, resolved, dismissed
    admin_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    post = relationship("CommunityPost")
    comment = relationship("CommunityComment")
    reported_user = relationship("User", foreign_keys=[reported_user_id])
    reporter = relationship("User", foreign_keys=[reporter_id])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<CommunityReport(id={self.id}, reason='{self.reason}')>"

class CommunityExpert(Base):
    __tablename__ = "community_experts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # 专家信息
    expertise_areas = Column(Text, nullable=False)  # JSON格式存储专业领域
    certification_level = Column(String(50), default="verified")  # verified, senior, master
    bio = Column(Text, nullable=True)  # 专家简介
    achievements = Column(Text, nullable=True)  # JSON格式存储成就
    
    # 统计信息
    answer_count = Column(Integer, default=0)
    best_answer_count = Column(Integer, default=0)
    helpful_votes = Column(Integer, default=0)
    reputation_score = Column(Float, default=0.0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User")
    
    def __repr__(self):
        return f"<CommunityExpert(id={self.id}, user_id={self.user_id})>"
