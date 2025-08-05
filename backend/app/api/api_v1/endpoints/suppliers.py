from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.services.supplier_service import SupplierService
from app.schemas.supplier import (
    Supplier, SupplierCreate, SupplierUpdate, SupplierQuery,
    SupplierStats, SupplierSummary
)
from app.models.user import User as UserModel
from app.models.supplier import SupplierType, SupplierScale, CertificationLevel

router = APIRouter()

@router.get("/", response_model=List[Supplier])
async def get_suppliers(
    country: Optional[str] = Query(None, description="按国家过滤"),
    supplier_type: Optional[SupplierType] = Query(None, description="按供应商类型过滤"),
    scale: Optional[SupplierScale] = Query(None, description="按企业规模过滤"),
    certification_level: Optional[CertificationLevel] = Query(None, description="按认证级别过滤"),
    product_category: Optional[str] = Query(None, description="按产品类别过滤"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="最低评分"),
    is_verified: Optional[bool] = Query(None, description="是否已验证"),
    is_featured: Optional[bool] = Query(None, description="是否推荐"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    sort_by: str = Query("overall_rating", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db)
):
    """获取供应商列表 - 公开访问"""
    query = SupplierQuery(
        country=country,
        supplier_type=supplier_type,
        scale=scale,
        certification_level=certification_level,
        product_category=product_category,
        keyword=keyword,
        min_rating=min_rating,
        is_verified=is_verified,
        is_featured=is_featured,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return SupplierService.get_suppliers(db, query)

@router.get("/stats", response_model=SupplierStats)
async def get_supplier_stats(db: Session = Depends(get_db)):
    """获取供应商统计信息 - 公开访问"""
    return SupplierService.get_supplier_stats(db)

@router.get("/featured", response_model=List[Supplier])
async def get_featured_suppliers(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取推荐供应商 - 公开访问"""
    return SupplierService.get_featured_suppliers(db, limit)

@router.get("/top-rated", response_model=List[Supplier])
async def get_top_rated_suppliers(
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取高评分供应商 - 公开访问"""
    return SupplierService.get_top_rated_suppliers(db, limit)

@router.get("/search", response_model=List[Supplier])
async def search_suppliers(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """搜索供应商 - 公开访问"""
    return SupplierService.search_suppliers(db, q, limit)

@router.get("/{supplier_id}", response_model=Supplier)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """获取单个供应商详情 - 公开访问"""
    supplier = SupplierService.get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )
    return supplier

@router.post("/", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier_data: SupplierCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """创建新供应商（仅管理员）"""
    return SupplierService.create_supplier(db, supplier_data, current_user.id)

@router.put("/{supplier_id}", response_model=Supplier)
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """更新供应商（仅管理员）"""
    supplier = SupplierService.update_supplier(db, supplier_id, supplier_update)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )
    return supplier

@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """删除供应商（仅管理员）"""
    success = SupplierService.delete_supplier(db, supplier_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )
    return {"message": "供应商删除成功"}
