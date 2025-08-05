from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.compliance_tool_service import ComplianceToolService
from app.schemas.compliance_tool import (
    ComplianceTool, ComplianceToolCreate, ComplianceToolUpdate,
    ComplianceToolQuery, ComplianceToolStats, ComplianceToolSummary,
    ToolUsageLogCreate, ToolReviewCreate, ToolReview
)
from app.models.user import User as UserModel
from app.models.compliance_tool import (
    ToolType, ToolCategory, ToolStatus, AccessLevel
)

router = APIRouter()

@router.get("/", response_model=List[ComplianceTool])
async def get_compliance_tools(
    tool_type: Optional[ToolType] = Query(None, description="工具类型"),
    category: Optional[ToolCategory] = Query(None, description="工具分类"),
    status: Optional[ToolStatus] = Query(None, description="工具状态"),
    access_level: Optional[AccessLevel] = Query(None, description="访问级别"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    vendor: Optional[str] = Query(None, description="供应商"),
    is_featured: Optional[bool] = Query(None, description="是否推荐"),
    is_verified: Optional[bool] = Query(None, description="是否已验证"),
    is_popular: Optional[bool] = Query(None, description="是否热门"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="最低评分"),
    max_price: Optional[float] = Query(None, ge=0.0, description="最高价格"),
    trial_available: Optional[bool] = Query(None, description="是否提供试用"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取合规工具列表 - 公开访问"""
    query = ComplianceToolQuery(
        tool_type=tool_type,
        category=category,
        status=status,
        access_level=access_level,
        keyword=keyword,
        vendor=vendor,
        is_featured=is_featured,
        is_verified=is_verified,
        is_popular=is_popular,
        min_rating=min_rating,
        max_price=max_price,
        trial_available=trial_available,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return ComplianceToolService.get_tools_list(db, query)

@router.get("/stats", response_model=ComplianceToolStats)
async def get_tool_stats(db: Session = Depends(get_db)):
    """获取合规工具统计信息 - 公开访问"""
    return ComplianceToolService.get_tool_stats(db)

@router.get("/featured", response_model=List[ComplianceTool])
async def get_featured_tools(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取推荐合规工具 - 公开访问"""
    return ComplianceToolService.get_featured_tools(db, limit)

@router.get("/popular", response_model=List[ComplianceTool])
async def get_popular_tools(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取热门合规工具 - 公开访问"""
    return ComplianceToolService.get_popular_tools(db, limit)

@router.get("/free", response_model=List[ComplianceTool])
async def get_free_tools(
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取免费合规工具 - 公开访问"""
    return ComplianceToolService.get_free_tools(db, limit)

@router.get("/search", response_model=List[ComplianceTool])
async def search_tools(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索合规工具 - 公开访问"""
    return ComplianceToolService.search_tools(db, q, limit)

@router.get("/{tool_id}", response_model=ComplianceTool)
async def get_tool_detail(
    tool_id: int,
    db: Session = Depends(get_db)
):
    """获取合规工具详情 - 公开访问"""
    tool = ComplianceToolService.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合规工具不存在"
        )
    return tool

@router.post("/", response_model=ComplianceTool, status_code=status.HTTP_201_CREATED)
async def create_tool(
    tool_data: ComplianceToolCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """创建合规工具（仅管理员）"""
    return ComplianceToolService.create_tool(db, tool_data, current_user.id)

@router.put("/{tool_id}", response_model=ComplianceTool)
async def update_tool(
    tool_id: int,
    tool_update: ComplianceToolUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """更新合规工具（仅管理员）"""
    tool = ComplianceToolService.update_tool(db, tool_id, tool_update)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合规工具不存在"
        )
    return tool

@router.delete("/{tool_id}")
async def delete_tool(
    tool_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """删除合规工具（仅管理员）"""
    success = ComplianceToolService.delete_tool(db, tool_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合规工具不存在"
        )
    return {"message": "合规工具删除成功"}

@router.post("/{tool_id}/use")
async def use_tool(
    tool_id: int,
    usage_data: ToolUsageLogCreate,
    request: Request,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """使用合规工具（需要登录）"""
    usage_data.tool_id = tool_id

    # 获取客户端信息
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    usage_log = ComplianceToolService.log_tool_usage(
        db, usage_data, current_user.id, ip_address, user_agent
    )

    return {"message": "工具使用记录已保存", "usage_id": usage_log.id}

@router.post("/{tool_id}/reviews", response_model=ToolReview)
async def add_tool_review(
    tool_id: int,
    review_data: ToolReviewCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """添加工具评价（需要登录）"""
    review_data.tool_id = tool_id
    return ComplianceToolService.add_tool_review(db, review_data, current_user.id)
