from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.models.community import (
    CommunityPost, CommunityComment, CommunityLike, CommunityCommentLike,
    CommunityFavorite, CommunityCategory, CommunityReport, CommunityExpert,
    PostType, PostStatus, PostPriority
)
from app.models.user import User
from app.schemas.community import (
    CommunityPostCreate, CommunityPostUpdate, CommunityPostQuery,
    CommunityStats, CommunityCommentCreate, CommunityLikeCreate,
    CommunityFavoriteCreate, CommunityCategoryCreate
)

class CommunityService:
    
    @staticmethod
    def create_post(
        db: Session, 
        post_data: CommunityPostCreate, 
        created_by: int
    ) -> CommunityPost:
        """创建新帖子"""
        db_post = CommunityPost(
            **post_data.model_dump(),
            created_by=created_by,
            published_at=datetime.utcnow() if post_data.post_type != PostType.DISCUSSION else None
        )
        db.add(db_post)
        
        # 更新分类帖子数量
        if post_data.category_id:
            category = db.query(CommunityCategory).filter(
                CommunityCategory.id == post_data.category_id
            ).first()
            if category:
                category.post_count += 1
        
        db.commit()
        db.refresh(db_post)
        return db_post
    
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> Optional[CommunityPost]:
        """根据ID获取帖子"""
        return db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    
    @staticmethod
    def get_posts_list(db: Session, query: CommunityPostQuery) -> List[CommunityPost]:
        """获取帖子列表"""
        db_query = db.query(CommunityPost)
        
        # 应用过滤条件
        if query.post_type:
            db_query = db_query.filter(CommunityPost.post_type == query.post_type)
        
        if query.status:
            db_query = db_query.filter(CommunityPost.status == query.status)
        else:
            # 默认只显示已发布的帖子
            db_query = db_query.filter(CommunityPost.status == PostStatus.PUBLISHED)
        
        if query.priority:
            db_query = db_query.filter(CommunityPost.priority == query.priority)
        
        if query.category_id:
            db_query = db_query.filter(CommunityPost.category_id == query.category_id)
        
        if query.author_id:
            db_query = db_query.filter(CommunityPost.created_by == query.author_id)
        
        if query.keyword:
            keyword_filter = or_(
                CommunityPost.title.contains(query.keyword),
                CommunityPost.content.contains(query.keyword),
                CommunityPost.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        if query.is_featured is not None:
            db_query = db_query.filter(CommunityPost.is_featured == query.is_featured)
        
        if query.is_official is not None:
            db_query = db_query.filter(CommunityPost.is_official == query.is_official)
        
        if query.is_expert_verified is not None:
            db_query = db_query.filter(CommunityPost.is_expert_verified == query.is_expert_verified)
        
        if query.is_hot is not None:
            db_query = db_query.filter(CommunityPost.is_hot == query.is_hot)

        if query.is_urgent is not None:
            db_query = db_query.filter(CommunityPost.is_urgent == query.is_urgent)

        if query.is_solved is not None:
            db_query = db_query.filter(CommunityPost.is_solved == query.is_solved)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(CommunityPost, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(CommunityPost, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_post(
        db: Session, 
        post_id: int, 
        post_update: CommunityPostUpdate,
        user_id: Optional[int] = None
    ) -> Optional[CommunityPost]:
        """更新帖子"""
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == post_id
        ).first()
        if not db_post:
            return None
        
        # 检查权限（只有作者可以修改）
        if user_id and db_post.created_by != user_id:
            return None
        
        update_data = post_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)
        
        db_post.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_post)
        return db_post
    
    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: Optional[int] = None) -> bool:
        """删除帖子"""
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == post_id
        ).first()
        if not db_post:
            return False
        
        # 检查权限（只有作者可以删除）
        if user_id and db_post.created_by != user_id:
            return False
        
        # 软删除
        db_post.status = PostStatus.DELETED
        db.commit()
        return True
    
    @staticmethod
    def get_community_stats(db: Session) -> CommunityStats:
        """获取社区统计信息"""
        # 总帖子数
        total_posts = db.query(CommunityPost).count()
        
        # 活跃帖子数
        active_posts = db.query(CommunityPost).filter(
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()
        
        # 按类型统计
        by_type = {}
        type_stats = db.query(
            CommunityPost.post_type,
            func.count(CommunityPost.id).label('count')
        ).filter(
            CommunityPost.status == PostStatus.PUBLISHED
        ).group_by(CommunityPost.post_type).all()
        
        for post_type, count in type_stats:
            by_type[post_type.value] = count
        
        # 按分类统计
        by_category = {}
        category_stats = db.query(
            CommunityCategory.name,
            func.count(CommunityPost.id).label('count')
        ).join(
            CommunityPost, CommunityPost.category_id == CommunityCategory.id
        ).filter(
            CommunityPost.status == PostStatus.PUBLISHED
        ).group_by(CommunityCategory.name).all()
        
        for category_name, count in category_stats:
            by_category[category_name] = count
        
        # 按优先级统计
        by_priority = {}
        priority_stats = db.query(
            CommunityPost.priority,
            func.count(CommunityPost.id).label('count')
        ).filter(
            CommunityPost.status == PostStatus.PUBLISHED
        ).group_by(CommunityPost.priority).all()
        
        for priority, count in priority_stats:
            by_priority[priority.value] = count
        
        # 特殊标记统计
        featured_count = db.query(CommunityPost).filter(
            CommunityPost.is_featured == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()
        
        official_count = db.query(CommunityPost).filter(
            CommunityPost.is_official == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()
        
        expert_verified_count = db.query(CommunityPost).filter(
            CommunityPost.is_expert_verified == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()
        
        hot_count = db.query(CommunityPost).filter(
            CommunityPost.is_hot == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()

        urgent_count = db.query(CommunityPost).filter(
            CommunityPost.is_urgent == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()

        solved_count = db.query(CommunityPost).filter(
            CommunityPost.is_solved == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).count()
        
        # 总浏览量、评论数、点赞数
        total_views = db.query(func.sum(CommunityPost.view_count)).scalar() or 0
        total_comments = db.query(func.sum(CommunityPost.comment_count)).scalar() or 0
        total_likes = db.query(func.sum(CommunityPost.like_count)).scalar() or 0
        
        return CommunityStats(
            total_posts=total_posts,
            active_posts=active_posts,
            by_type=by_type,
            by_category=by_category,
            by_priority=by_priority,
            featured_count=featured_count,
            official_count=official_count,
            expert_verified_count=expert_verified_count,
            hot_count=hot_count,
            urgent_count=urgent_count,
            solved_count=solved_count,
            total_views=total_views,
            total_comments=total_comments,
            total_likes=total_likes
        )
    
    @staticmethod
    def get_featured_posts(db: Session, limit: int = 10) -> List[CommunityPost]:
        """获取推荐帖子"""
        return db.query(CommunityPost).filter(
            CommunityPost.is_featured == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).order_by(desc(CommunityPost.last_activity_at)).limit(limit).all()
    
    @staticmethod
    def get_hot_posts(db: Session, limit: int = 10) -> List[CommunityPost]:
        """获取热门帖子"""
        return db.query(CommunityPost).filter(
            CommunityPost.is_hot == True,
            CommunityPost.status == PostStatus.PUBLISHED
        ).order_by(desc(CommunityPost.view_count)).limit(limit).all()
    
    @staticmethod
    def get_latest_posts(db: Session, limit: int = 20) -> List[CommunityPost]:
        """获取最新帖子"""
        return db.query(CommunityPost).filter(
            CommunityPost.status == PostStatus.PUBLISHED
        ).order_by(desc(CommunityPost.created_at)).limit(limit).all()
    
    @staticmethod
    def get_trending_posts(db: Session, days: int = 7, limit: int = 10) -> List[CommunityPost]:
        """获取趋势帖子（基于最近活跃度）"""
        since_date = datetime.utcnow() - timedelta(days=days)
        return db.query(CommunityPost).filter(
            CommunityPost.status == PostStatus.PUBLISHED,
            CommunityPost.last_activity_at >= since_date
        ).order_by(
            desc(CommunityPost.like_count + CommunityPost.comment_count * 2)
        ).limit(limit).all()
    
    @staticmethod
    def search_posts(db: Session, search_term: str, limit: int = 20) -> List[CommunityPost]:
        """搜索帖子"""
        search_filter = or_(
            CommunityPost.title.contains(search_term),
            CommunityPost.content.contains(search_term),
            CommunityPost.keywords.contains(search_term)
        )
        
        return db.query(CommunityPost).filter(
            CommunityPost.status == PostStatus.PUBLISHED,
            search_filter
        ).order_by(desc(CommunityPost.last_activity_at)).limit(limit).all()
    
    @staticmethod
    def increment_view_count(db: Session, post_id: int) -> bool:
        """增加浏览次数"""
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == post_id
        ).first()
        if not db_post:
            return False
        
        db_post.view_count += 1
        db.commit()
        return True
    
    @staticmethod
    def create_comment(
        db: Session, 
        comment_data: CommunityCommentCreate, 
        user_id: int
    ) -> CommunityComment:
        """创建评论"""
        db_comment = CommunityComment(
            **comment_data.model_dump(),
            created_by=user_id
        )
        db.add(db_comment)
        
        # 更新帖子评论数
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == comment_data.post_id
        ).first()
        if db_post:
            db_post.comment_count += 1
            db_post.last_activity_at = datetime.utcnow()
        
        # 如果是回复评论，更新父评论回复数
        if comment_data.parent_id:
            parent_comment = db.query(CommunityComment).filter(
                CommunityComment.id == comment_data.parent_id
            ).first()
            if parent_comment:
                parent_comment.reply_count += 1
        
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def toggle_like(
        db: Session, 
        like_data: CommunityLikeCreate, 
        user_id: int
    ) -> CommunityLike:
        """切换点赞状态"""
        # 检查是否已点赞
        existing_like = db.query(CommunityLike).filter(
            CommunityLike.post_id == like_data.post_id,
            CommunityLike.user_id == user_id
        ).first()
        
        if existing_like:
            # 如果已存在，更新状态
            existing_like.is_like = like_data.is_like
            db_like = existing_like
        else:
            # 创建新的点赞记录
            db_like = CommunityLike(
                post_id=like_data.post_id,
                user_id=user_id,
                is_like=like_data.is_like
            )
            db.add(db_like)
        
        # 更新帖子点赞数
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == like_data.post_id
        ).first()
        if db_post:
            # 重新计算点赞数
            like_count = db.query(CommunityLike).filter(
                CommunityLike.post_id == like_data.post_id,
                CommunityLike.is_like == True
            ).count()
            dislike_count = db.query(CommunityLike).filter(
                CommunityLike.post_id == like_data.post_id,
                CommunityLike.is_like == False
            ).count()
            
            db_post.like_count = like_count
            db_post.dislike_count = dislike_count
        
        db.commit()
        db.refresh(db_like)
        return db_like
    
    @staticmethod
    def add_to_favorites(
        db: Session, 
        favorite_data: CommunityFavoriteCreate, 
        user_id: int
    ) -> CommunityFavorite:
        """添加到收藏"""
        # 检查是否已收藏
        existing = db.query(CommunityFavorite).filter(
            CommunityFavorite.post_id == favorite_data.post_id,
            CommunityFavorite.user_id == user_id
        ).first()
        
        if existing:
            return existing
        
        db_favorite = CommunityFavorite(
            **favorite_data.model_dump(),
            user_id=user_id
        )
        db.add(db_favorite)
        
        # 更新帖子收藏数
        db_post = db.query(CommunityPost).filter(
            CommunityPost.id == favorite_data.post_id
        ).first()
        if db_post:
            db_post.favorite_count += 1
        
        db.commit()
        db.refresh(db_favorite)
        return db_favorite
