from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.supplier import Supplier, SupplierType, SupplierScale, CertificationLevel
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierQuery, SupplierStats

class SupplierService:
    
    @staticmethod
    def create_supplier(db: Session, supplier_data: SupplierCreate, created_by: Optional[int] = None) -> Supplier:
        """创建新供应商"""
        db_supplier = Supplier(
            **supplier_data.model_dump(),
            created_by=created_by
        )
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    
    @staticmethod
    def get_supplier_by_id(db: Session, supplier_id: int) -> Optional[Supplier]:
        """根据ID获取供应商"""
        return db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_active == True).first()
    
    @staticmethod
    def get_suppliers(db: Session, query: SupplierQuery) -> List[Supplier]:
        """获取供应商列表"""
        db_query = db.query(Supplier).filter(Supplier.is_active == True)
        
        # 应用过滤条件
        if query.country:
            db_query = db_query.filter(Supplier.country == query.country)
        
        if query.supplier_type:
            db_query = db_query.filter(Supplier.supplier_type == query.supplier_type)
        
        if query.scale:
            db_query = db_query.filter(Supplier.scale == query.scale)
        
        if query.certification_level:
            db_query = db_query.filter(Supplier.certification_level == query.certification_level)
        
        if query.product_category:
            db_query = db_query.filter(Supplier.product_categories.contains(query.product_category))
        
        if query.keyword:
            keyword_filter = or_(
                Supplier.company_name.contains(query.keyword),
                Supplier.company_name_en.contains(query.keyword),
                Supplier.main_products.contains(query.keyword),
                Supplier.keywords.contains(query.keyword)
            )
            db_query = db_query.filter(keyword_filter)
        
        if query.min_rating is not None:
            db_query = db_query.filter(Supplier.overall_rating >= query.min_rating)
        
        if query.is_verified is not None:
            db_query = db_query.filter(Supplier.is_verified == query.is_verified)
        
        if query.is_featured is not None:
            db_query = db_query.filter(Supplier.is_featured == query.is_featured)
        
        # 排序
        if query.sort_order == "desc":
            db_query = db_query.order_by(desc(getattr(Supplier, query.sort_by)))
        else:
            db_query = db_query.order_by(asc(getattr(Supplier, query.sort_by)))
        
        # 分页
        return db_query.offset(query.skip).limit(query.limit).all()
    
    @staticmethod
    def update_supplier(db: Session, supplier_id: int, supplier_update: SupplierUpdate) -> Optional[Supplier]:
        """更新供应商"""
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_active == True).first()
        if not db_supplier:
            return None
        
        update_data = supplier_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_supplier, field, value)
        
        db_supplier.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    
    @staticmethod
    def delete_supplier(db: Session, supplier_id: int) -> bool:
        """软删除供应商"""
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_active == True).first()
        if not db_supplier:
            return False
        
        db_supplier.is_active = False
        db_supplier.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def get_supplier_stats(db: Session) -> SupplierStats:
        """获取供应商统计信息"""
        # 总供应商数
        total_suppliers = db.query(Supplier).filter(Supplier.is_active == True).count()
        
        # 按国家统计
        by_country = {}
        country_stats = db.query(
            Supplier.country, 
            func.count(Supplier.id).label('count')
        ).filter(Supplier.is_active == True).group_by(Supplier.country).all()
        
        for country, count in country_stats:
            by_country[country] = count
        
        # 按类型统计
        by_type = {}
        type_stats = db.query(
            Supplier.supplier_type, 
            func.count(Supplier.id).label('count')
        ).filter(Supplier.is_active == True).group_by(Supplier.supplier_type).all()
        
        for supplier_type, count in type_stats:
            by_type[supplier_type.value] = count
        
        # 按规模统计
        by_scale = {}
        scale_stats = db.query(
            Supplier.scale, 
            func.count(Supplier.id).label('count')
        ).filter(Supplier.is_active == True).group_by(Supplier.scale).all()
        
        for scale, count in scale_stats:
            by_scale[scale.value] = count
        
        # 按认证级别统计
        by_certification = {}
        cert_stats = db.query(
            Supplier.certification_level, 
            func.count(Supplier.id).label('count')
        ).filter(Supplier.is_active == True).group_by(Supplier.certification_level).all()
        
        for cert_level, count in cert_stats:
            by_certification[cert_level.value] = count
        
        # 已验证供应商数
        verified_count = db.query(Supplier).filter(
            Supplier.is_active == True,
            Supplier.is_verified == True
        ).count()
        
        # 推荐供应商数
        featured_count = db.query(Supplier).filter(
            Supplier.is_active == True,
            Supplier.is_featured == True
        ).count()
        
        # 平均评分
        avg_rating_result = db.query(func.avg(Supplier.overall_rating)).filter(
            Supplier.is_active == True,
            Supplier.overall_rating > 0
        ).scalar()
        avg_rating = float(avg_rating_result) if avg_rating_result else 0.0
        
        return SupplierStats(
            total_suppliers=total_suppliers,
            by_country=by_country,
            by_type=by_type,
            by_scale=by_scale,
            by_certification=by_certification,
            verified_count=verified_count,
            featured_count=featured_count,
            avg_rating=round(avg_rating, 2)
        )
    
    @staticmethod
    def get_featured_suppliers(db: Session, limit: int = 10) -> List[Supplier]:
        """获取推荐供应商"""
        return db.query(Supplier).filter(
            Supplier.is_active == True,
            Supplier.is_featured == True
        ).order_by(desc(Supplier.overall_rating)).limit(limit).all()
    
    @staticmethod
    def get_top_rated_suppliers(db: Session, limit: int = 10) -> List[Supplier]:
        """获取高评分供应商"""
        return db.query(Supplier).filter(
            Supplier.is_active == True,
            Supplier.overall_rating >= 4.0,
            Supplier.review_count >= 5
        ).order_by(desc(Supplier.overall_rating)).limit(limit).all()
    
    @staticmethod
    def search_suppliers(db: Session, search_term: str, limit: int = 20) -> List[Supplier]:
        """搜索供应商"""
        search_filter = or_(
            Supplier.company_name.contains(search_term),
            Supplier.company_name_en.contains(search_term),
            Supplier.main_products.contains(search_term),
            Supplier.product_categories.contains(search_term),
            Supplier.keywords.contains(search_term)
        )
        
        return db.query(Supplier).filter(
            Supplier.is_active == True,
            search_filter
        ).order_by(desc(Supplier.overall_rating)).limit(limit).all()
    
    @staticmethod
    def get_suppliers_by_country(db: Session, country: str, limit: int = 20) -> List[Supplier]:
        """按国家获取供应商"""
        return db.query(Supplier).filter(
            Supplier.is_active == True,
            Supplier.country == country
        ).order_by(desc(Supplier.overall_rating)).limit(limit).all()
