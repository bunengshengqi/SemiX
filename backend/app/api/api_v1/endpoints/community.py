from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.community_service import CommunityService
from app.schemas.community import (
    CommunityPost, CommunityPostCreate, CommunityPostUpdate,
    CommunityPostQuery, CommunityStats, CommunityPostSummary,
    CommunityComment, CommunityCommentCreate, CommunityLikeCreate,
    CommunityFavoriteCreate, CommunityCategory, CommunityCategoryCreate
)
from app.models.user import User as UserModel
from app.models.community import (
    PostType, PostStatus, PostPriority
)

router = APIRouter()

@router.get("/", response_model=List[CommunityPost])
async def get_community_posts(
    post_type: Optional[PostType] = Query(None, description="帖子类型"),
    status: Optional[PostStatus] = Query(None, description="帖子状态"),
    priority: Optional[PostPriority] = Query(None, description="优先级"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    author_id: Optional[int] = Query(None, description="作者ID"),
    is_featured: Optional[bool] = Query(None, description="是否推荐"),
    is_official: Optional[bool] = Query(None, description="是否官方"),
    is_expert_verified: Optional[bool] = Query(None, description="是否专家认证"),
    is_hot: Optional[bool] = Query(None, description="是否热门"),
    is_urgent: Optional[bool] = Query(None, description="是否紧急"),
    is_solved: Optional[bool] = Query(None, description="是否已解决"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("last_activity_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取社区帖子列表 - 公开访问"""
    query = CommunityPostQuery(
        post_type=post_type,
        status=status,
        priority=priority,
        category_id=category_id,
        keyword=keyword,
        author_id=author_id,
        is_featured=is_featured,
        is_official=is_official,
        is_expert_verified=is_expert_verified,
        is_hot=is_hot,
        is_urgent=is_urgent,
        is_solved=is_solved,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return CommunityService.get_posts_list(db, query)

@router.get("/stats", response_model=CommunityStats)
async def get_community_stats(db: Session = Depends(get_db)):
    """获取社区统计信息 - 公开访问"""
    return CommunityService.get_community_stats(db)

@router.get("/featured", response_model=List[CommunityPost])
async def get_featured_posts(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取推荐帖子 - 公开访问"""
    return CommunityService.get_featured_posts(db, limit)

@router.get("/hot", response_model=List[CommunityPost])
async def get_hot_posts(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取热门帖子 - 公开访问"""
    return CommunityService.get_hot_posts(db, limit)

@router.get("/latest", response_model=List[CommunityPost])
async def get_latest_posts(
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取最新帖子 - 公开访问"""
    return CommunityService.get_latest_posts(db, limit)

@router.get("/trending", response_model=List[CommunityPost])
async def get_trending_posts(
    days: int = Query(7, ge=1, le=30, description="天数范围"),
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取趋势帖子 - 公开访问"""
    return CommunityService.get_trending_posts(db, days, limit)

@router.get("/search", response_model=List[CommunityPost])
async def search_posts(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索帖子 - 公开访问"""
    return CommunityService.search_posts(db, q, limit)

@router.get("/{post_id}", response_model=CommunityPost)
async def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db)
):
    """获取帖子详情 - 公开访问"""
    post = CommunityService.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )

    # 增加浏览次数
    CommunityService.increment_view_count(db, post_id)

    return post

@router.post("/", response_model=CommunityPost, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: CommunityPostCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建帖子（需要登录）"""
    return CommunityService.create_post(db, post_data, current_user.id)

@router.put("/{post_id}", response_model=CommunityPost)
async def update_post(
    post_id: int,
    post_update: CommunityPostUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新帖子（仅作者）"""
    post = CommunityService.update_post(db, post_id, post_update, current_user.id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权限修改"
        )
    return post

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除帖子（仅作者）"""
    success = CommunityService.delete_post(db, post_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权限删除"
        )
    return {"message": "帖子删除成功"}

@router.post("/{post_id}/comments", response_model=CommunityComment)
async def create_comment(
    post_id: int,
    comment_data: CommunityCommentCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建评论（需要登录）"""
    comment_data.post_id = post_id
    return CommunityService.create_comment(db, comment_data, current_user.id)

@router.post("/{post_id}/likes")
async def toggle_like(
    post_id: int,
    is_like: bool = Query(True, description="True=点赞, False=点踩"),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """切换点赞状态（需要登录）"""
    like_data = CommunityLikeCreate(post_id=post_id, is_like=is_like)
    like = CommunityService.toggle_like(db, like_data, current_user.id)
    return {"message": f"{'点赞' if is_like else '点踩'}成功", "like_id": like.id}

@router.post("/{post_id}/favorites")
async def add_to_favorites(
    post_id: int,
    folder_name: Optional[str] = Query(None, description="收藏夹名称"),
    notes: Optional[str] = Query(None, description="收藏备注"),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """添加到收藏（需要登录）"""
    favorite_data = CommunityFavoriteCreate(
        post_id=post_id,
        folder_name=folder_name,
        notes=notes
    )
    favorite = CommunityService.add_to_favorites(db, favorite_data, current_user.id)
    return {"message": "收藏成功", "favorite_id": favorite.id}

# 管理员专用接口
@router.patch("/{post_id}/feature")
async def feature_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """推荐帖子（仅管理员）"""
    post_update = CommunityPostUpdate(is_featured=True)
    post = CommunityService.update_post(db, post_id, post_update)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    return {"message": "帖子已设为推荐"}

@router.patch("/{post_id}/official")
async def mark_official(
    post_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """标记为官方帖子（仅管理员）"""
    post_update = CommunityPostUpdate(is_official=True)
    post = CommunityService.update_post(db, post_id, post_update)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    return {"message": "帖子已标记为官方"}

@router.patch("/{post_id}/solved")
async def mark_solved(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """标记为已解决（作者或管理员）"""
    post_update = CommunityPostUpdate(is_solved=True)
    post = CommunityService.update_post(db, post_id, post_update, current_user.id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权限修改"
        )
    return {"message": "问题已标记为解决"}
