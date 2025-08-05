#!/usr/bin/env python3
"""
简化的数据库初始化脚本
"""
import os
import sys
from datetime import datetime
import json

# 设置环境变量使用SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./semix.db'

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User
from app.models.policy import Policy, PolicyUrgency, PolicyStatus, PolicyCategory

def init_database():
    """初始化数据库"""
    print("🚀 开始初始化数据库...")
    
    # 创建数据库表
    try:
        create_tables()
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
        return False
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建admin用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@semix.com",
                full_name="系统管理员",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("✅ Admin用户创建成功")
        else:
            print("ℹ️  Admin用户已存在")
        
        # 检查是否已有政策数据
        existing_policies = db.query(Policy).count()
        if existing_policies > 0:
            print(f"ℹ️  已存在 {existing_policies} 条政策数据")
            return True
        
        # 创建政策数据 - 包含30+条数据
        policies = [
            # 日本政策 (8条)
            {
                "title": "日本半导体制造设备出口管制新规",
                "summary": "日本政府针对先进制程半导体制造设备实施新的出口管制措施，涉及23类设备",
                "content": "根据日本经济产业省最新公告，自2024年7月起，对23类先进半导体制造设备实施出口许可制度。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.EXPORT_CONTROL,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "METI-2024-001",
                "effective_date": datetime(2024, 7, 1),
                "impact_score": 85,
                "affected_industries": json.dumps(["半导体制造", "设备制造", "材料供应"]),
                "source_name": "经济产业省",
                "tags": json.dumps(["出口管制", "半导体设备", "先进制程"]),
                "keywords": "半导体,制造设备,出口管制,许可证",
                "created_by": admin_user.id
            },
            {
                "title": "日本半导体战略推进政策",
                "summary": "日本政府发布半导体产业振兴战略，计划投资2万亿日元支持本土半导体产业发展",
                "content": "日本政府制定了全面的半导体产业振兴计划，包括支持台积电在熊本建厂、推进Rapidus先进制程项目等。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "METI-2024-002",
                "effective_date": datetime(2024, 4, 1),
                "impact_score": 90,
                "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "封装测试"]),
                "source_name": "经济产业省",
                "tags": json.dumps(["产业政策", "投资支持", "半导体战略"]),
                "keywords": "半导体,产业振兴,投资,台积电,Rapidus",
                "created_by": admin_user.id
            },
            {
                "title": "日本数字化转型税收优惠政策",
                "summary": "日本推出数字化转型税收优惠政策，支持企业数字化升级改造",
                "content": "为促进企业数字化转型，日本政府推出税收优惠政策，对数字化投资给予税额抵减。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.TAXATION,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "METI-2024-003",
                "effective_date": datetime(2024, 5, 1),
                "impact_score": 60,
                "affected_industries": json.dumps(["信息技术", "制造业", "服务业"]),
                "source_name": "经济产业省",
                "tags": json.dumps(["数字化转型", "税收优惠", "技术升级"]),
                "keywords": "数字化,税收优惠,技术升级,投资",
                "created_by": admin_user.id
            },
            {
                "title": "日本绿色能源半导体支持计划",
                "summary": "日本推出绿色能源半导体支持计划，重点支持功率半导体和新能源汽车芯片",
                "content": "为实现碳中和目标，日本政府推出绿色能源半导体支持计划，重点支持SiC、GaN等功率半导体发展。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "METI-2024-004",
                "effective_date": datetime(2024, 6, 1),
                "impact_score": 75,
                "affected_industries": json.dumps(["功率半导体", "新能源汽车", "可再生能源"]),
                "source_name": "经济产业省",
                "tags": json.dumps(["绿色能源", "功率半导体", "碳中和"]),
                "keywords": "功率半导体,绿色能源,SiC,GaN,新能源汽车",
                "created_by": admin_user.id
            },
            {
                "title": "日本半导体人才培养计划",
                "summary": "日本启动半导体人才培养计划，加强产学研合作培养高端半导体人才",
                "content": "日本政府与大学、企业合作，启动半导体人才培养计划，重点培养先进制程和设计人才。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MEXT-2024-001",
                "effective_date": datetime(2024, 4, 1),
                "impact_score": 70,
                "affected_industries": json.dumps(["半导体制造", "IC设计", "教育培训"]),
                "source_name": "文部科学省",
                "tags": json.dumps(["人才培养", "产学研合作", "教育"]),
                "keywords": "人才培养,半导体,产学研,教育,技能",
                "created_by": admin_user.id
            },
            {
                "title": "日本半导体材料出口促进政策",
                "summary": "日本推出半导体材料出口促进政策，支持高端材料企业拓展海外市场",
                "content": "为提升日本半导体材料的国际竞争力，政府推出出口促进政策，提供融资和市场开拓支持。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.TRADE_POLICY,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "JETRO-2024-001",
                "effective_date": datetime(2024, 3, 1),
                "impact_score": 65,
                "affected_industries": json.dumps(["半导体材料", "化学工业", "出口贸易"]),
                "source_name": "日本贸易振兴机构",
                "tags": json.dumps(["出口促进", "半导体材料", "市场开拓"]),
                "keywords": "半导体材料,出口,市场开拓,融资支持",
                "created_by": admin_user.id
            },
            {
                "title": "日本量子技术发展战略",
                "summary": "日本发布量子技术发展战略，重点发展量子计算和量子通信技术",
                "content": "日本政府发布量子技术发展战略，计划在量子计算、量子通信等领域加大投资。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "CAO-2024-001",
                "effective_date": datetime(2024, 2, 1),
                "impact_score": 80,
                "affected_industries": json.dumps(["量子技术", "半导体", "通信技术"]),
                "source_name": "内阁府",
                "tags": json.dumps(["量子技术", "前沿科技", "战略投资"]),
                "keywords": "量子计算,量子通信,前沿技术,战略投资",
                "created_by": admin_user.id
            },
            {
                "title": "日本AI芯片发展支持政策",
                "summary": "日本推出AI芯片发展支持政策，重点支持边缘AI和自动驾驶芯片",
                "content": "为抢占AI芯片市场，日本政府推出支持政策，重点发展边缘AI芯片和自动驾驶专用芯片。",
                "country": "日本",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "METI-2024-005",
                "effective_date": datetime(2024, 5, 15),
                "impact_score": 75,
                "affected_industries": json.dumps(["AI芯片", "自动驾驶", "边缘计算"]),
                "source_name": "经济产业省",
                "tags": json.dumps(["AI芯片", "边缘计算", "自动驾驶"]),
                "keywords": "AI芯片,边缘计算,自动驾驶,人工智能",
                "created_by": admin_user.id
            },

            # 韩国政策 (8条)
            {
                "title": "韩国K-半导体带政策更新",
                "summary": "韩国政府更新K-半导体带政策，新增税收减免措施和研发支持计划",
                "content": "韩国政府对K-半导体带政策进行重大更新：企业所得税减免从15%提高到25%。",
                "country": "韩国",
                "region": "京畿道、忠清南道",
                "category": PolicyCategory.TAXATION,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-003",
                "effective_date": datetime(2024, 6, 1),
                "impact_score": 80,
                "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["税收优惠", "K-半导体带", "投资支持"]),
                "keywords": "K-半导体带,税收减免,投资支持,研发",
                "created_by": admin_user.id
            },
            {
                "title": "韩国半导体材料国产化支持政策",
                "summary": "韩国推出半导体核心材料国产化支持计划，重点支持光刻胶、电子气体等关键材料",
                "content": "为减少对日本半导体材料的依赖，韩国政府推出材料国产化支持计划，设立1万亿韩元基金。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-004",
                "effective_date": datetime(2024, 5, 15),
                "impact_score": 85,
                "affected_industries": json.dumps(["半导体材料", "化学工业", "精密化工"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["材料国产化", "技术自立", "供应链安全"]),
                "keywords": "半导体材料,国产化,光刻胶,电子气体",
                "created_by": admin_user.id
            },
            {
                "title": "韩国存储半导体技术创新计划",
                "summary": "韩国推出存储半导体技术创新计划，重点发展下一代存储技术",
                "content": "韩国政府推出存储半导体技术创新计划，重点发展MRAM、ReRAM等新型存储技术。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-005",
                "effective_date": datetime(2024, 4, 1),
                "impact_score": 75,
                "affected_industries": json.dumps(["存储半导体", "新型存储", "技术研发"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["存储技术", "技术创新", "下一代存储"]),
                "keywords": "存储半导体,MRAM,ReRAM,新型存储",
                "created_by": admin_user.id
            },
            {
                "title": "韩国半导体设备产业育成政策",
                "summary": "韩国推出半导体设备产业育成政策，支持本土设备企业技术升级",
                "content": "为提升韩国半导体设备产业竞争力，政府推出产业育成政策，提供技术开发和市场拓展支持。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-006",
                "effective_date": datetime(2024, 3, 15),
                "impact_score": 70,
                "affected_industries": json.dumps(["半导体设备", "制造业", "技术服务"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["设备产业", "技术升级", "产业育成"]),
                "keywords": "半导体设备,产业育成,技术升级,竞争力",
                "created_by": admin_user.id
            },
            {
                "title": "韩国系统半导体发展战略",
                "summary": "韩国发布系统半导体发展战略，重点发展汽车、IoT、AI芯片",
                "content": "韩国政府发布系统半导体发展战略，计划在汽车芯片、IoT芯片、AI芯片等领域实现突破。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-007",
                "effective_date": datetime(2024, 2, 1),
                "impact_score": 85,
                "affected_industries": json.dumps(["系统半导体", "汽车芯片", "IoT", "AI芯片"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["系统半导体", "汽车芯片", "IoT", "AI"]),
                "keywords": "系统半导体,汽车芯片,IoT,AI芯片",
                "created_by": admin_user.id
            },
            {
                "title": "韩国半导体人才培养强化方案",
                "summary": "韩国推出半导体人才培养强化方案，扩大半导体专业招生规模",
                "content": "为解决半导体人才短缺问题，韩国政府推出人才培养强化方案，扩大大学半导体专业招生。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOE-2024-001",
                "effective_date": datetime(2024, 3, 1),
                "impact_score": 65,
                "affected_industries": json.dumps(["半导体", "教育", "人才培养"]),
                "source_name": "教育部",
                "tags": json.dumps(["人才培养", "教育", "专业建设"]),
                "keywords": "人才培养,半导体专业,教育,招生",
                "created_by": admin_user.id
            },
            {
                "title": "韩国半导体出口金融支持政策",
                "summary": "韩国推出半导体出口金融支持政策，为半导体企业提供出口信贷和保险",
                "content": "为支持半导体企业拓展海外市场，韩国政府推出出口金融支持政策，提供优惠信贷和保险。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.TRADE_POLICY,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "KOTRA-2024-001",
                "effective_date": datetime(2024, 4, 15),
                "impact_score": 60,
                "affected_industries": json.dumps(["半导体", "出口贸易", "金融服务"]),
                "source_name": "韩国贸易投资振兴公社",
                "tags": json.dumps(["出口支持", "金融服务", "贸易促进"]),
                "keywords": "出口金融,信贷,保险,贸易支持",
                "created_by": admin_user.id
            },
            {
                "title": "韩国半导体供应链安全强化政策",
                "summary": "韩国推出半导体供应链安全强化政策，建立供应链风险监测体系",
                "content": "为应对供应链风险，韩国政府推出供应链安全强化政策，建立风险监测和应急响应机制。",
                "country": "韩国",
                "region": "全国",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOTIE-2024-008",
                "effective_date": datetime(2024, 6, 15),
                "impact_score": 80,
                "affected_industries": json.dumps(["半导体", "供应链", "风险管理"]),
                "source_name": "产业通商资源部",
                "tags": json.dumps(["供应链安全", "风险监测", "应急响应"]),
                "keywords": "供应链,安全,风险监测,应急响应",
                "created_by": admin_user.id
            },

            # 台湾省政策 (8条)
            {
                "title": "台湾省半导体先进制程发展计划",
                "summary": "台湾省推出半导体先进制程发展计划，支持2纳米以下制程技术研发和产业化",
                "content": "台湾省科技部门推出半导体先进制程发展计划：投资3000亿新台币支持先进制程研发。",
                "country": "台湾省",
                "region": "新竹、台中、台南",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOST-2024-001",
                "effective_date": datetime(2024, 1, 1),
                "impact_score": 95,
                "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "IC设计"]),
                "source_name": "科技部门",
                "tags": json.dumps(["先进制程", "技术研发", "产业升级"]),
                "keywords": "先进制程,2纳米,技术研发,产业化",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省半导体产业链韧性强化政策",
                "summary": "台湾省推出半导体产业链韧性强化政策，提升供应链安全和自主可控能力",
                "content": "为应对全球供应链挑战，台湾省推出产业链韧性强化政策：建立关键材料战略储备。",
                "country": "台湾省",
                "region": "全省",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOEA-2024-002",
                "effective_date": datetime(2024, 4, 15),
                "impact_score": 85,
                "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "封装测试"]),
                "source_name": "经济部门",
                "tags": json.dumps(["供应链安全", "产业韧性", "自主可控"]),
                "keywords": "供应链,韧性,战略储备,风险监测",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省IC设计产业发展计划",
                "summary": "台湾省推出IC设计产业发展计划，重点支持AI芯片和5G芯片设计",
                "content": "台湾省推出IC设计产业发展计划，重点支持AI芯片、5G芯片等高端芯片设计。",
                "country": "台湾省",
                "region": "新竹科学园区",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOEA-2024-003",
                "effective_date": datetime(2024, 3, 1),
                "impact_score": 80,
                "affected_industries": json.dumps(["IC设计", "AI芯片", "5G芯片"]),
                "source_name": "经济部门",
                "tags": json.dumps(["IC设计", "AI芯片", "5G"]),
                "keywords": "IC设计,AI芯片,5G芯片,高端设计",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省半导体封装测试升级计划",
                "summary": "台湾省推出半导体封装测试升级计划，发展先进封装技术",
                "content": "台湾省推出封装测试升级计划，重点发展系统级封装(SiP)、扇出型封装等先进技术。",
                "country": "台湾省",
                "region": "高雄、台中",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOEA-2024-004",
                "effective_date": datetime(2024, 5, 1),
                "impact_score": 75,
                "affected_industries": json.dumps(["封装测试", "先进封装", "系统集成"]),
                "source_name": "经济部门",
                "tags": json.dumps(["先进封装", "SiP", "扇出型封装"]),
                "keywords": "先进封装,SiP,扇出型封装,系统级封装",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省半导体设备自主化推进计划",
                "summary": "台湾省推出半导体设备自主化推进计划，减少对进口设备的依赖",
                "content": "台湾省推出设备自主化推进计划，支持本土设备企业技术创新和产业化。",
                "country": "台湾省",
                "region": "全省",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOEA-2024-005",
                "effective_date": datetime(2024, 2, 15),
                "impact_score": 80,
                "affected_industries": json.dumps(["半导体设备", "制造业", "技术创新"]),
                "source_name": "经济部门",
                "tags": json.dumps(["设备自主化", "技术创新", "产业升级"]),
                "keywords": "设备自主化,技术创新,本土设备,产业化",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省半导体人才留用计划",
                "summary": "台湾省推出半导体人才留用计划，防止人才流失到海外",
                "content": "为防止半导体人才流失，台湾省推出人才留用计划，提供优厚待遇和发展机会。",
                "country": "台湾省",
                "region": "全省",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOL-2024-001",
                "effective_date": datetime(2024, 4, 1),
                "impact_score": 70,
                "affected_industries": json.dumps(["半导体", "人才服务", "教育培训"]),
                "source_name": "劳动部门",
                "tags": json.dumps(["人才留用", "人才政策", "待遇优化"]),
                "keywords": "人才留用,人才政策,待遇,发展机会",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省绿色半导体制造推进政策",
                "summary": "台湾省推出绿色半导体制造推进政策，促进半导体产业绿色转型",
                "content": "台湾省推出绿色制造推进政策，支持半导体企业采用清洁能源和绿色制造技术。",
                "country": "台湾省",
                "region": "全省",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "EPA-2024-001",
                "effective_date": datetime(2024, 6, 1),
                "impact_score": 65,
                "affected_industries": json.dumps(["半导体制造", "清洁能源", "环保技术"]),
                "source_name": "环保部门",
                "tags": json.dumps(["绿色制造", "清洁能源", "环保"]),
                "keywords": "绿色制造,清洁能源,环保,可持续发展",
                "created_by": admin_user.id
            },
            {
                "title": "台湾省半导体国际合作促进政策",
                "summary": "台湾省推出半导体国际合作促进政策，加强与全球伙伴的技术合作",
                "content": "台湾省推出国际合作促进政策，加强与美国、欧洲等地区的半导体技术合作。",
                "country": "台湾省",
                "region": "全省",
                "category": PolicyCategory.TRADE_POLICY,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MOFA-2024-001",
                "effective_date": datetime(2024, 3, 15),
                "impact_score": 60,
                "affected_industries": json.dumps(["半导体", "国际贸易", "技术合作"]),
                "source_name": "外交部门",
                "tags": json.dumps(["国际合作", "技术合作", "全球伙伴"]),
                "keywords": "国际合作,技术合作,全球伙伴,贸易",
                "created_by": admin_user.id
            },

            # 东南亚政策 (10条)
            {
                "title": "新加坡半导体制造激励计划",
                "summary": "新加坡推出新一轮半导体制造激励计划，吸引全球半导体企业在新加坡设立制造基地",
                "content": "新加坡经济发展局推出半导体制造激励计划：提供最高30%的投资津贴。",
                "country": "东南亚",
                "region": "新加坡",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "EDB-2024-001",
                "effective_date": datetime(2024, 3, 1),
                "impact_score": 70,
                "affected_industries": json.dumps(["半导体制造", "封装测试", "设备制造"]),
                "source_name": "经济发展局",
                "tags": json.dumps(["投资激励", "制造业", "税收优惠"]),
                "keywords": "半导体制造,投资激励,税收优惠,先进封装",
                "created_by": admin_user.id
            },
            {
                "title": "马来西亚半导体封装测试中心建设计划",
                "summary": "马来西亚推出半导体封装测试中心建设计划，打造东南亚封装测试枢纽",
                "content": "马来西亚政府推出封装测试中心建设计划，重点发展槟城和吉隆坡的封装测试产业。",
                "country": "东南亚",
                "region": "马来西亚",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MITI-2024-001",
                "effective_date": datetime(2024, 4, 1),
                "impact_score": 75,
                "affected_industries": json.dumps(["封装测试", "半导体制造", "电子制造"]),
                "source_name": "国际贸易和工业部",
                "tags": json.dumps(["封装测试", "产业集群", "制造中心"]),
                "keywords": "封装测试,产业集群,制造中心,槟城",
                "created_by": admin_user.id
            },
            {
                "title": "泰国电子产业升级支持政策",
                "summary": "泰国推出电子产业升级支持政策，重点发展汽车电子和智能制造",
                "content": "泰国政府推出电子产业升级支持政策，重点支持汽车电子、智能制造等高附加值产业。",
                "country": "东南亚",
                "region": "泰国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "BOI-2024-001",
                "effective_date": datetime(2024, 5, 1),
                "impact_score": 65,
                "affected_industries": json.dumps(["汽车电子", "智能制造", "电子产业"]),
                "source_name": "投资促进委员会",
                "tags": json.dumps(["产业升级", "汽车电子", "智能制造"]),
                "keywords": "产业升级,汽车电子,智能制造,高附加值",
                "created_by": admin_user.id
            },
            {
                "title": "越南半导体产业发展战略",
                "summary": "越南发布半导体产业发展战略，计划建设半导体产业园区",
                "content": "越南政府发布半导体产业发展战略，计划在胡志明市和河内建设半导体产业园区。",
                "country": "东南亚",
                "region": "越南",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.HIGH,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MPI-2024-001",
                "effective_date": datetime(2024, 2, 1),
                "impact_score": 80,
                "affected_industries": json.dumps(["半导体", "电子制造", "产业园区"]),
                "source_name": "计划投资部",
                "tags": json.dumps(["产业发展", "产业园区", "战略规划"]),
                "keywords": "半导体产业,产业园区,胡志明市,河内",
                "created_by": admin_user.id
            },
            {
                "title": "印尼电子制造业投资促进政策",
                "summary": "印尼推出电子制造业投资促进政策，吸引外资投资电子产业",
                "content": "印尼政府推出电子制造业投资促进政策，为外资企业提供税收优惠和土地使用便利。",
                "country": "东南亚",
                "region": "印尼",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "BKPM-2024-001",
                "effective_date": datetime(2024, 3, 15),
                "impact_score": 60,
                "affected_industries": json.dumps(["电子制造", "外商投资", "制造业"]),
                "source_name": "投资协调委员会",
                "tags": json.dumps(["投资促进", "外资", "电子制造"]),
                "keywords": "电子制造,外资投资,税收优惠,土地使用",
                "created_by": admin_user.id
            },
            {
                "title": "菲律宾IT-BPM产业发展计划",
                "summary": "菲律宾推出IT-BPM产业发展计划，重点发展软件服务和数据处理",
                "content": "菲律宾政府推出IT-BPM产业发展计划，重点发展软件外包、数据处理等服务业。",
                "country": "东南亚",
                "region": "菲律宾",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "DTI-2024-001",
                "effective_date": datetime(2024, 4, 15),
                "impact_score": 55,
                "affected_industries": json.dumps(["IT服务", "软件外包", "数据处理"]),
                "source_name": "贸易工业部",
                "tags": json.dumps(["IT服务", "软件外包", "服务业"]),
                "keywords": "IT服务,软件外包,数据处理,BPM",
                "created_by": admin_user.id
            },
            {
                "title": "新加坡数字经济转型支持政策",
                "summary": "新加坡推出数字经济转型支持政策，重点支持半导体企业数字化升级",
                "content": "新加坡资讯通信媒体发展局推出数字经济转型支持政策：数字化转型补贴最高80%。",
                "country": "东南亚",
                "region": "新加坡",
                "category": PolicyCategory.REGULATION,
                "urgency": PolicyUrgency.LOW,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "IMDA-2024-001",
                "effective_date": datetime(2024, 2, 1),
                "impact_score": 60,
                "affected_industries": json.dumps(["半导体制造", "软件服务", "数据分析"]),
                "source_name": "资讯通信媒体发展局",
                "tags": json.dumps(["数字化转型", "智能制造", "工业4.0"]),
                "keywords": "数字化转型,智能制造,人工智能,工业4.0",
                "created_by": admin_user.id
            },
            {
                "title": "马来西亚电动汽车产业发展政策",
                "summary": "马来西亚推出电动汽车产业发展政策，重点发展汽车电子和电池技术",
                "content": "马来西亚政府推出电动汽车产业发展政策，重点发展汽车电子芯片和电池管理系统。",
                "country": "东南亚",
                "region": "马来西亚",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "MITI-2024-002",
                "effective_date": datetime(2024, 5, 15),
                "impact_score": 70,
                "affected_industries": json.dumps(["电动汽车", "汽车电子", "电池技术"]),
                "source_name": "国际贸易和工业部",
                "tags": json.dumps(["电动汽车", "汽车电子", "电池技术"]),
                "keywords": "电动汽车,汽车电子,电池管理,新能源",
                "created_by": admin_user.id
            },
            {
                "title": "泰国智慧城市建设计划",
                "summary": "泰国推出智慧城市建设计划，重点发展物联网和智能基础设施",
                "content": "泰国政府推出智慧城市建设计划，重点发展物联网技术和智能基础设施建设。",
                "country": "东南亚",
                "region": "泰国",
                "category": PolicyCategory.INVESTMENT,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "DEPA-2024-001",
                "effective_date": datetime(2024, 6, 1),
                "impact_score": 65,
                "affected_industries": json.dumps(["物联网", "智能基础设施", "信息技术"]),
                "source_name": "数字经济促进局",
                "tags": json.dumps(["智慧城市", "物联网", "智能基础设施"]),
                "keywords": "智慧城市,物联网,智能基础设施,数字化",
                "created_by": admin_user.id
            },
            {
                "title": "ASEAN半导体产业合作框架",
                "summary": "ASEAN推出半导体产业合作框架，促进区域内半导体产业协同发展",
                "content": "ASEAN推出半导体产业合作框架，促进成员国在半导体领域的技术合作和产业协同。",
                "country": "东南亚",
                "region": "ASEAN",
                "category": PolicyCategory.TRADE_POLICY,
                "urgency": PolicyUrgency.MEDIUM,
                "status": PolicyStatus.PUBLISHED,
                "policy_number": "ASEAN-2024-001",
                "effective_date": datetime(2024, 1, 1),
                "impact_score": 75,
                "affected_industries": json.dumps(["半导体", "区域合作", "技术合作"]),
                "source_name": "ASEAN秘书处",
                "tags": json.dumps(["区域合作", "产业协同", "技术合作"]),
                "keywords": "ASEAN,区域合作,产业协同,技术合作",
                "created_by": admin_user.id
            }
        ]
        
        # 批量创建政策
        for policy_data in policies:
            policy = Policy(**policy_data)
            db.add(policy)
        
        db.commit()
        print(f"✅ 创建了 {len(policies)} 条政策数据")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据初始化失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 数据库初始化完成！")
        print("Admin账号信息：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("  邮箱: admin@semix.com")
        print("\n数据库文件: semix.db")
    else:
        print("\n❌ 数据库初始化失败！")
        sys.exit(1)
