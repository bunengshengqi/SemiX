#!/usr/bin/env python3
"""
合规工具数据初始化脚本 - 创建合规工具数据
"""
import os
import sys
from datetime import datetime, timedelta
import json
import random

# 设置环境变量使用SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./semix.db'

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.models.user import User
from app.models.compliance_tool import (
    ComplianceTool, ToolType, ToolCategory, ToolStatus, AccessLevel
)

def create_compliance_tools_data(db: Session):
    """创建合规工具数据"""
    
    # 检查是否已有合规工具数据
    existing_tools = db.query(ComplianceTool).count()
    if existing_tools > 0:
        print(f"已存在 {existing_tools} 条合规工具数据")
        return
    
    # 获取admin用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        print("❌ 未找到admin用户，请先运行 init_db.py")
        return
    
    # 合规工具数据
    tools_data = [
        # 法规检查器类工具 (8条)
        {
            "name": "半导体出口管制检查器",
            "name_en": "Semiconductor Export Control Checker",
            "description": "自动检查半导体产品是否受到出口管制限制，支持美国EAR、欧盟双用途物项清单等多个管制清单的查询和分析。",
            "short_description": "检查半导体产品出口管制状态，支持多国管制清单",
            "tool_type": ToolType.REGULATION_CHECKER,
            "category": ToolCategory.TRADE_COMPLIANCE,
            "status": ToolStatus.ACTIVE,
            "access_level": AccessLevel.PREMIUM,
            "applicable_regions": json.dumps(["美国", "欧盟", "日本", "韩国", "中国"]),
            "applicable_industries": json.dumps(["半导体", "电子", "通信设备"]),
            "applicable_products": json.dumps(["集成电路", "处理器", "存储器", "传感器"]),
            "features": json.dumps([
                "实时管制清单查询",
                "产品分类自动识别",
                "许可证要求分析",
                "风险等级评估",
                "合规建议生成"
            ]),
            "input_requirements": "产品型号、技术参数、目的国家",
            "output_format": "PDF报告、Excel表格、API响应",
            "usage_guide": "1. 输入产品信息 2. 选择目的国 3. 系统自动分析 4. 生成合规报告",
            "examples": json.dumps([
                "检查CPU出口到俄罗斯的管制状态",
                "分析GPU是否需要出口许可证",
                "评估存储芯片的双用途风险"
            ]),
            "api_endpoint": "/api/tools/export-control-check",
            "documentation_url": "https://docs.semix.com/tools/export-control",
            "version": "2.1.0",
            "last_updated": datetime.now() - timedelta(days=5),
            "dependencies": json.dumps(["出口管制数据库", "产品分类系统"]),
            "system_requirements": "支持REST API调用，需要网络连接",
            "rating": 4.7,
            "usage_count": 1250,
            "download_count": 890,
            "review_count": 45,
            "tags": json.dumps(["出口管制", "EAR", "双用途", "许可证"]),
            "keywords": "出口管制,EAR,ECCN,许可证,双用途物项",
            "price": 299.0,
            "pricing_model": "按月订阅",
            "trial_available": True,
            "vendor": "SemiX合规科技",
            "contact_email": "compliance@semix.com",
            "support_url": "https://support.semix.com/export-control",
            "compliance_standards": json.dumps(["EAR", "ITAR", "EU Dual-Use Regulation"]),
            "audit_trail": True,
            "is_featured": True,
            "is_verified": True,
            "is_popular": True,
            "created_by": admin_user.id
        },
        {
            "name": "HS编码智能查询工具",
            "name_en": "HS Code Intelligent Lookup Tool",
            "description": "基于AI技术的HS编码查询工具，支持产品描述自动匹配、多语言识别、历史查询记录等功能，提高报关效率。",
            "short_description": "AI驱动的HS编码查询，支持自动匹配和多语言识别",
            "tool_type": ToolType.REGULATION_CHECKER,
            "category": ToolCategory.CUSTOMS,
            "status": ToolStatus.ACTIVE,
            "access_level": AccessLevel.FREE,
            "applicable_regions": json.dumps(["全球"]),
            "applicable_industries": json.dumps(["进出口贸易", "物流", "制造业"]),
            "applicable_products": json.dumps(["所有商品"]),
            "features": json.dumps([
                "AI智能匹配",
                "多语言支持",
                "历史查询记录",
                "相似产品推荐",
                "税率信息查询"
            ]),
            "input_requirements": "产品名称或描述",
            "output_format": "HS编码、产品描述、税率信息",
            "usage_guide": "输入产品描述，系统自动匹配最合适的HS编码",
            "examples": json.dumps([
                "查询'集成电路'的HS编码",
                "匹配'智能手机'的商品编码",
                "识别'LED显示屏'的分类"
            ]),
            "api_endpoint": "/api/tools/hs-code-lookup",
            "documentation_url": "https://docs.semix.com/tools/hs-code",
            "version": "1.5.2",
            "last_updated": datetime.now() - timedelta(days=12),
            "rating": 4.3,
            "usage_count": 5680,
            "download_count": 2340,
            "review_count": 128,
            "tags": json.dumps(["HS编码", "海关", "报关", "AI"]),
            "keywords": "HS编码,海关编码,商品分类,报关",
            "price": 0.0,
            "pricing_model": "免费使用",
            "trial_available": False,
            "vendor": "SemiX合规科技",
            "contact_email": "support@semix.com",
            "support_url": "https://support.semix.com/hs-code",
            "compliance_standards": json.dumps(["WCO HS Convention"]),
            "audit_trail": False,
            "is_featured": True,
            "is_verified": True,
            "is_popular": True,
            "created_by": admin_user.id
        },
        
        # 文档模板类工具 (6条)
        {
            "name": "合规文档模板库",
            "name_en": "Compliance Document Template Library",
            "description": "提供各类合规文档模板，包括出口许可申请、质量认证文件、环保声明等，支持自定义编辑和批量生成。",
            "short_description": "丰富的合规文档模板，支持自定义编辑和批量生成",
            "tool_type": ToolType.DOCUMENT_TEMPLATE,
            "category": ToolCategory.TRADE_COMPLIANCE,
            "status": ToolStatus.ACTIVE,
            "access_level": AccessLevel.PREMIUM,
            "applicable_regions": json.dumps(["全球"]),
            "applicable_industries": json.dumps(["制造业", "贸易", "物流"]),
            "applicable_products": json.dumps(["所有产品"]),
            "features": json.dumps([
                "200+专业模板",
                "自定义编辑器",
                "批量生成功能",
                "多语言版本",
                "电子签名支持"
            ]),
            "input_requirements": "企业信息、产品信息、交易详情",
            "output_format": "Word文档、PDF文件",
            "usage_guide": "选择模板类型，填写相关信息，生成标准文档",
            "examples": json.dumps([
                "生成出口许可申请表",
                "创建产品合规声明",
                "制作质量认证文件"
            ]),
            "api_endpoint": "/api/tools/document-templates",
            "documentation_url": "https://docs.semix.com/tools/templates",
            "version": "3.0.1",
            "last_updated": datetime.now() - timedelta(days=8),
            "rating": 4.5,
            "usage_count": 2890,
            "download_count": 1560,
            "review_count": 67,
            "tags": json.dumps(["文档模板", "合规文件", "批量生成"]),
            "keywords": "文档模板,合规文件,许可申请,认证文件",
            "price": 199.0,
            "pricing_model": "按年订阅",
            "trial_available": True,
            "vendor": "SemiX合规科技",
            "contact_email": "templates@semix.com",
            "support_url": "https://support.semix.com/templates",
            "compliance_standards": json.dumps(["ISO 9001", "ISO 14001"]),
            "audit_trail": True,
            "is_featured": True,
            "is_verified": True,
            "is_popular": False,
            "created_by": admin_user.id
        },
        
        # 关税计算器类工具 (4条)
        {
            "name": "智能关税计算器",
            "name_en": "Smart Tariff Calculator",
            "description": "精确计算进出口关税、增值税、消费税等各项税费，支持多国税率查询、优惠政策识别、成本分析等功能。",
            "short_description": "精确计算进出口税费，支持多国税率和优惠政策",
            "tool_type": ToolType.TARIFF_CALCULATOR,
            "category": ToolCategory.CUSTOMS,
            "status": ToolStatus.ACTIVE,
            "access_level": AccessLevel.FREE,
            "applicable_regions": json.dumps(["中国", "美国", "欧盟", "日本", "韩国"]),
            "applicable_industries": json.dumps(["进出口贸易", "制造业", "电商"]),
            "applicable_products": json.dumps(["所有商品"]),
            "features": json.dumps([
                "实时税率查询",
                "优惠政策识别",
                "成本分析报告",
                "汇率自动更新",
                "批量计算支持"
            ]),
            "input_requirements": "HS编码、商品价值、原产国、目的国",
            "output_format": "详细税费清单、成本分析报告",
            "usage_guide": "输入商品信息和贸易路线，系统自动计算各项税费",
            "examples": json.dumps([
                "计算手机从中国出口到美国的关税",
                "分析芯片进口到欧盟的总成本",
                "比较不同贸易协定下的税率差异"
            ]),
            "api_endpoint": "/api/tools/tariff-calculator",
            "documentation_url": "https://docs.semix.com/tools/tariff",
            "version": "2.3.0",
            "last_updated": datetime.now() - timedelta(days=3),
            "rating": 4.6,
            "usage_count": 8920,
            "download_count": 3450,
            "review_count": 234,
            "tags": json.dumps(["关税计算", "税费", "成本分析", "贸易"]),
            "keywords": "关税,税费,进出口,成本计算,贸易",
            "price": 0.0,
            "pricing_model": "免费使用",
            "trial_available": False,
            "vendor": "SemiX合规科技",
            "contact_email": "tariff@semix.com",
            "support_url": "https://support.semix.com/tariff",
            "compliance_standards": json.dumps(["WTO Agreement", "FTA Rules"]),
            "audit_trail": False,
            "is_featured": True,
            "is_verified": True,
            "is_popular": True,
            "created_by": admin_user.id
        },
        
        # 风险评估类工具 (5条)
        {
            "name": "供应链合规风险评估",
            "name_en": "Supply Chain Compliance Risk Assessment",
            "description": "全面评估供应链合规风险，包括供应商背景调查、制裁清单筛查、ESG评估、地缘政治风险分析等。",
            "short_description": "全面的供应链合规风险评估和管理工具",
            "tool_type": ToolType.RISK_ASSESSMENT,
            "category": ToolCategory.TRADE_COMPLIANCE,
            "status": ToolStatus.ACTIVE,
            "access_level": AccessLevel.ENTERPRISE,
            "applicable_regions": json.dumps(["全球"]),
            "applicable_industries": json.dumps(["制造业", "贸易", "物流", "金融"]),
            "applicable_products": json.dumps(["所有产品"]),
            "features": json.dumps([
                "供应商背景调查",
                "制裁清单筛查",
                "ESG风险评估",
                "地缘政治分析",
                "风险监控预警"
            ]),
            "input_requirements": "供应商信息、交易数据、产品信息",
            "output_format": "风险评估报告、监控仪表板",
            "usage_guide": "输入供应商和交易信息，系统进行全面风险分析",
            "examples": json.dumps([
                "评估新供应商的合规风险",
                "监控现有供应链的风险变化",
                "分析地缘政治对供应链的影响"
            ]),
            "api_endpoint": "/api/tools/risk-assessment",
            "documentation_url": "https://docs.semix.com/tools/risk",
            "version": "1.8.0",
            "last_updated": datetime.now() - timedelta(days=15),
            "rating": 4.8,
            "usage_count": 1560,
            "download_count": 780,
            "review_count": 89,
            "tags": json.dumps(["风险评估", "供应链", "制裁筛查", "ESG"]),
            "keywords": "风险评估,供应链,制裁,ESG,合规",
            "price": 999.0,
            "pricing_model": "企业定制",
            "trial_available": True,
            "vendor": "SemiX合规科技",
            "contact_email": "risk@semix.com",
            "support_url": "https://support.semix.com/risk",
            "compliance_standards": json.dumps(["OFAC", "EU Sanctions", "UN Sanctions"]),
            "audit_trail": True,
            "is_featured": True,
            "is_verified": True,
            "is_popular": False,
            "created_by": admin_user.id
        }
    ]
    
    # 生成更多随机工具数据
    additional_tools = generate_additional_tools(admin_user.id, len(tools_data))
    tools_data.extend(additional_tools)
    
    print(f"准备创建 {len(tools_data)} 条合规工具数据...")
    
    # 批量创建合规工具
    for tool_data in tools_data:
        tool = ComplianceTool(**tool_data)
        db.add(tool)
    
    db.commit()
    print(f"✅ 创建了 {len(tools_data)} 条合规工具数据")

def generate_additional_tools(admin_user_id: int, existing_count: int):
    """生成额外的合规工具数据"""
    
    additional_tools = []
    
    # 工具模板
    tool_templates = [
        {
            "name_template": "{}合规检查工具",
            "type": ToolType.REGULATION_CHECKER,
            "categories": [ToolCategory.TRADE_COMPLIANCE, ToolCategory.PRODUCT_SAFETY, ToolCategory.ENVIRONMENTAL],
            "access_levels": [AccessLevel.FREE, AccessLevel.PREMIUM]
        },
        {
            "name_template": "{}文档生成器",
            "type": ToolType.DOCUMENT_TEMPLATE,
            "categories": [ToolCategory.TRADE_COMPLIANCE, ToolCategory.CUSTOMS],
            "access_levels": [AccessLevel.PREMIUM, AccessLevel.ENTERPRISE]
        },
        {
            "name_template": "{}风险评估系统",
            "type": ToolType.RISK_ASSESSMENT,
            "categories": [ToolCategory.TRADE_COMPLIANCE, ToolCategory.FINANCIAL],
            "access_levels": [AccessLevel.PREMIUM, AccessLevel.ENTERPRISE]
        }
    ]
    
    domains = ["环保", "数据隐私", "劳动法", "知识产权", "产品安全", "财务", "海关", "贸易"]
    vendors = ["SemiX合规科技", "全球合规解决方案", "智能合规系统", "合规专家", "法规科技"]
    
    # 生成剩余工具
    for i in range(existing_count, 30):  # 生成30个工具
        template = random.choice(tool_templates)
        domain = random.choice(domains)
        
        tool_data = {
            "name": template["name_template"].format(domain),
            "name_en": f"{domain} Compliance Tool {i+1}",
            "description": f"专业的{domain}合规工具，提供全面的合规检查和管理功能。支持自动化检查、报告生成、风险评估等多项功能，帮助企业确保{domain}合规。",
            "short_description": f"专业的{domain}合规工具，支持自动化检查和管理",
            "tool_type": template["type"],
            "category": random.choice(template["categories"]),
            "status": ToolStatus.ACTIVE,
            "access_level": random.choice(template["access_levels"]),
            "applicable_regions": json.dumps(random.sample(["中国", "美国", "欧盟", "日本", "韩国", "全球"], 3)),
            "applicable_industries": json.dumps(random.sample(["制造业", "贸易", "物流", "金融", "科技"], 2)),
            "applicable_products": json.dumps([f"{domain}相关产品", "通用产品"]),
            "features": json.dumps([
                f"{domain}合规检查",
                "自动化分析",
                "报告生成",
                "风险评估",
                "合规建议"
            ]),
            "input_requirements": f"{domain}相关信息和数据",
            "output_format": "PDF报告、Excel表格",
            "usage_guide": f"输入{domain}相关信息，系统自动进行合规分析",
            "examples": json.dumps([f"{domain}合规检查示例{j+1}" for j in range(2)]),
            "api_endpoint": f"/api/tools/{domain.lower()}-compliance",
            "documentation_url": f"https://docs.semix.com/tools/{domain.lower()}",
            "version": f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
            "last_updated": datetime.now() - timedelta(days=random.randint(1, 30)),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "usage_count": random.randint(100, 5000),
            "download_count": random.randint(50, 2000),
            "review_count": random.randint(10, 200),
            "tags": json.dumps([domain, "合规", "检查", "工具"]),
            "keywords": f"{domain},合规,检查,工具,自动化",
            "price": round(random.uniform(0, 500), 0) if random.choice([True, False]) else 0.0,
            "pricing_model": random.choice(["免费使用", "按月订阅", "按年订阅", "一次性购买"]),
            "trial_available": random.choice([True, False]),
            "vendor": random.choice(vendors),
            "contact_email": f"support@{random.choice(['semix', 'compliance', 'legal'])}.com",
            "support_url": f"https://support.semix.com/{domain.lower()}",
            "compliance_standards": json.dumps([f"{domain}标准{j+1}" for j in range(2)]),
            "audit_trail": random.choice([True, False]),
            "is_featured": random.choice([True, False]),
            "is_verified": True,
            "is_popular": random.choice([True, False]),
            "created_by": admin_user_id
        }
        
        additional_tools.append(tool_data)
    
    return additional_tools

def main():
    """主函数"""
    print("🚀 开始初始化合规工具数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建合规工具数据
        create_compliance_tools_data(db)
        
        print("✅ 合规工具数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 合规工具数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
