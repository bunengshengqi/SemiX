from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, List

from app.core.database import get_db
from app.core.deps import get_current_superuser
from app.services.data_collection_service import DataCollectionService
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/start-collection")
async def start_data_collection(
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """启动数据采集任务（仅管理员）"""
    
    async def run_collection():
        collector = DataCollectionService()
        results = await collector.collect_from_multiple_sources()
        # 这里可以添加结果通知逻辑
        print(f"数据采集完成，共采集 {results['total_collected']} 条数据")
    
    background_tasks.add_task(run_collection)
    
    return {
        "message": "数据采集任务已启动",
        "status": "running",
        "initiated_by": current_user.username
    }

@router.get("/collection-status")
async def get_collection_status(
    current_user: UserModel = Depends(get_current_superuser)
):
    """获取数据采集状态"""
    # 这里可以实现真实的状态查询逻辑
    return {
        "status": "idle",  # idle, running, completed, failed
        "last_run": "2024-08-05T10:00:00Z",
        "total_collected": 1250,
        "sources": {
            "alibaba": {"status": "completed", "count": 450},
            "made_in_china": {"status": "completed", "count": 380},
            "enterprise_api": {"status": "completed", "count": 320},
            "industry_database": {"status": "completed", "count": 100}
        }
    }

@router.post("/manual-add-supplier")
async def manual_add_supplier(
    supplier_data: dict,
    current_user: UserModel = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """手动添加供应商数据"""
    try:
        collector = DataCollectionService()
        success = await collector._save_supplier_if_not_exists(db, supplier_data)
        
        if success:
            db.commit()
            return {"message": "供应商添加成功", "status": "success"}
        else:
            return {"message": "供应商已存在或数据无效", "status": "skipped"}
            
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"添加供应商失败: {str(e)}"
        )

@router.get("/data-sources")
async def get_available_data_sources():
    """获取可用的数据源列表"""
    return {
        "sources": [
            {
                "name": "alibaba",
                "display_name": "阿里巴巴",
                "type": "b2b_platform",
                "status": "available",
                "description": "全球最大的B2B平台，包含大量供应商信息",
                "estimated_records": 50000,
                "update_frequency": "daily"
            },
            {
                "name": "made_in_china",
                "display_name": "中国制造网",
                "type": "b2b_platform", 
                "status": "available",
                "description": "中国领先的B2B平台",
                "estimated_records": 30000,
                "update_frequency": "daily"
            },
            {
                "name": "enterprise_api",
                "display_name": "企业信息API",
                "type": "api_service",
                "status": "requires_key",
                "description": "企查查、天眼查等企业信息API",
                "estimated_records": 100000,
                "update_frequency": "real_time"
            },
            {
                "name": "industry_database",
                "display_name": "行业数据库",
                "type": "industry_data",
                "status": "available",
                "description": "半导体行业协会、展会等专业数据",
                "estimated_records": 5000,
                "update_frequency": "weekly"
            }
        ]
    }

@router.post("/configure-source")
async def configure_data_source(
    source_config: dict,
    current_user: UserModel = Depends(get_current_superuser)
):
    """配置数据源参数"""
    # 这里可以保存数据源配置，如API密钥、采集参数等
    return {
        "message": "数据源配置已保存",
        "source": source_config.get("source_name"),
        "status": "configured"
    }
