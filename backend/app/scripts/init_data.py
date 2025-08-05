"""
数据初始化脚本
创建admin用户和政策监控测试数据
"""
import sys
import os

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User
from app.models.policy import Policy, PolicyUrgency, PolicyStatus, PolicyCategory

def create_admin_user(db: Session):
    """创建admin用户"""
    # 检查是否已存在admin用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if admin_user:
        print("Admin用户已存在")
        return admin_user
    
    # 创建admin用户
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
    return admin_user

def create_policy_data(db: Session, admin_user: User):
    """创建政策监控测试数据"""
    
    # 检查是否已有政策数据
    existing_policies = db.query(Policy).count()
    if existing_policies > 0:
        print(f"已存在 {existing_policies} 条政策数据")
        return
    
    # 政策数据
    policies_data = [
        # 日本政策
        {
            "title": "半导体制造设备出口管制新规",
            "summary": "日本政府针对先进制程半导体制造设备实施新的出口管制措施，涉及23类设备",
            "content": "根据日本经济产业省最新公告，自2024年7月起，对23类先进半导体制造设备实施出口许可制度。包括极紫外光刻机、离子注入设备、化学气相沉积设备等关键设备。出口企业需要提前申请许可证，审批周期约为90天。",
            "country": "日本",
            "region": "全国",
            "category": PolicyCategory.EXPORT_CONTROL,
            "urgency": PolicyUrgency.HIGH,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "METI-2024-001",
            "effective_date": datetime(2024, 7, 1),
            "impact_score": 85,
            "affected_industries": json.dumps(["半导体制造", "设备制造", "材料供应"]),
            "source_url": "https://www.meti.go.jp/policy/anpo/semicon.html",
            "source_name": "经济产业省",
            "tags": json.dumps(["出口管制", "半导体设备", "先进制程"]),
            "keywords": "半导体,制造设备,出口管制,许可证"
        },
        {
            "title": "日本半导体战略推进政策",
            "summary": "日本政府发布半导体产业振兴战略，计划投资2万亿日元支持本土半导体产业发展",
            "content": "日本政府制定了全面的半导体产业振兴计划，包括：1）支持台积电在熊本建厂；2）推进Rapidus先进制程项目；3）加强半导体人才培养；4）建立半导体供应链联盟。政府将提供税收优惠、研发补贴等多项支持措施。",
            "country": "日本",
            "region": "全国",
            "category": PolicyCategory.INVESTMENT,
            "urgency": PolicyUrgency.MEDIUM,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "METI-2024-002",
            "effective_date": datetime(2024, 4, 1),
            "impact_score": 90,
            "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "封装测试"]),
            "source_url": "https://www.meti.go.jp/policy/mono_info_service/joho/semiconductor.html",
            "source_name": "经济产业省",
            "tags": json.dumps(["产业政策", "投资支持", "半导体战略"]),
            "keywords": "半导体,产业振兴,投资,台积电,Rapidus"
        },
        
        # 韩国政策
        {
            "title": "K-半导体带政策更新",
            "summary": "韩国政府更新K-半导体带政策，新增税收减免措施和研发支持计划",
            "content": "韩国政府对K-半导体带政策进行重大更新：1）企业所得税减免从15%提高到25%；2）新增设备投资税额抵减；3）扩大研发费用加计扣除比例；4）简化外国人才签证程序；5）加强产学研合作支持。政策适用于京畿道、忠清南道等半导体产业集群。",
            "country": "韩国",
            "region": "京畿道、忠清南道",
            "category": PolicyCategory.TAXATION,
            "urgency": PolicyUrgency.MEDIUM,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "MOTIE-2024-003",
            "effective_date": datetime(2024, 6, 1),
            "impact_score": 80,
            "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造"]),
            "source_url": "https://www.motie.go.kr/motie/ne/presse/press2/bbs/bbsView.do",
            "source_name": "产业通商资源部",
            "tags": json.dumps(["税收优惠", "K-半导体带", "投资支持"]),
            "keywords": "K-半导体带,税收减免,投资支持,研发"
        },
        {
            "title": "韩国半导体材料国产化支持政策",
            "summary": "韩国推出半导体核心材料国产化支持计划，重点支持光刻胶、电子气体等关键材料",
            "content": "为减少对日本半导体材料的依赖，韩国政府推出材料国产化支持计划：1）设立1万亿韩元材料国产化基金；2）支持本土企业技术研发；3）建立材料测试认证中心；4）推进产业链上下游合作；5）加强与海外技术合作。重点支持光刻胶、高纯度氟化氢、氟聚酰亚胺等核心材料。",
            "country": "韩国",
            "region": "全国",
            "category": PolicyCategory.INVESTMENT,
            "urgency": PolicyUrgency.HIGH,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "MOTIE-2024-004",
            "effective_date": datetime(2024, 5, 15),
            "impact_score": 75,
            "affected_industries": json.dumps(["半导体材料", "化学工业", "精密化工"]),
            "source_url": "https://www.motie.go.kr/motie/ne/presse/press2/bbs/bbsView.do",
            "source_name": "产业通商资源部",
            "tags": json.dumps(["材料国产化", "技术自立", "供应链安全"]),
            "keywords": "半导体材料,国产化,光刻胶,电子气体"
        },
        
        # 新加坡政策
        {
            "title": "新加坡半导体制造激励计划",
            "summary": "新加坡推出新一轮半导体制造激励计划，吸引全球半导体企业在新加坡设立制造基地",
            "content": "新加坡经济发展局推出半导体制造激励计划：1）提供最高30%的投资津贴；2）企业所得税优惠税率5-10%；3）加速折旧政策；4）研发支出双倍扣除；5）人才培训补贴；6）土地使用优惠。重点吸引先进封装、功率半导体、汽车芯片等领域投资。",
            "country": "新加坡",
            "region": "全国",
            "category": PolicyCategory.INVESTMENT,
            "urgency": PolicyUrgency.MEDIUM,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "EDB-2024-001",
            "effective_date": datetime(2024, 3, 1),
            "impact_score": 70,
            "affected_industries": json.dumps(["半导体制造", "封装测试", "设备制造"]),
            "source_url": "https://www.edb.gov.sg/en/our-industries/electronics.html",
            "source_name": "经济发展局",
            "tags": json.dumps(["投资激励", "制造业", "税收优惠"]),
            "keywords": "半导体制造,投资激励,税收优惠,先进封装"
        },
        {
            "title": "新加坡数字经济转型支持政策",
            "summary": "新加坡推出数字经济转型支持政策，重点支持半导体企业数字化升级",
            "content": "新加坡资讯通信媒体发展局推出数字经济转型支持政策：1）数字化转型补贴最高80%；2）人工智能应用支持；3）工业4.0技术推广；4）数据分析能力建设；5）网络安全防护支持。半导体企业可申请智能制造、供应链数字化等项目支持。",
            "country": "新加坡",
            "region": "全国",
            "category": PolicyCategory.REGULATION,
            "urgency": PolicyUrgency.LOW,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "IMDA-2024-001",
            "effective_date": datetime(2024, 2, 1),
            "impact_score": 60,
            "affected_industries": json.dumps(["半导体制造", "软件服务", "数据分析"]),
            "source_url": "https://www.imda.gov.sg/programme-listing/smes-go-digital",
            "source_name": "资讯通信媒体发展局",
            "tags": json.dumps(["数字化转型", "智能制造", "工业4.0"]),
            "keywords": "数字化转型,智能制造,人工智能,工业4.0"
        },
        
        # 台湾省政策
        {
            "title": "台湾省半导体先进制程发展计划",
            "summary": "台湾省推出半导体先进制程发展计划，支持2纳米以下制程技术研发和产业化",
            "content": "台湾省科技部门推出半导体先进制程发展计划：1）投资3000亿新台币支持先进制程研发；2）建设先进制程研发中心；3）培养高端半导体人才；4）加强产学研合作；5）推进关键材料和设备本土化。重点支持2纳米、1.4纳米制程技术开发。",
            "country": "台湾省",
            "region": "新竹、台中、台南",
            "category": PolicyCategory.INVESTMENT,
            "urgency": PolicyUrgency.HIGH,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "MOST-2024-001",
            "effective_date": datetime(2024, 1, 1),
            "impact_score": 95,
            "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "IC设计"]),
            "source_url": "https://www.most.gov.tw/",
            "source_name": "科技部门",
            "tags": json.dumps(["先进制程", "技术研发", "产业升级"]),
            "keywords": "先进制程,2纳米,技术研发,产业化"
        },
        {
            "title": "台湾省半导体产业链韧性强化政策",
            "summary": "台湾省推出半导体产业链韧性强化政策，提升供应链安全和自主可控能力",
            "content": "为应对全球供应链挑战，台湾省推出产业链韧性强化政策：1）建立关键材料战略储备；2）推进供应商多元化；3）加强供应链风险监测；4）支持关键技术自主研发；5）建立产业链合作联盟。重点关注光刻胶、电子气体、硅晶圆等关键材料供应安全。",
            "country": "台湾省",
            "region": "全省",
            "category": PolicyCategory.REGULATION,
            "urgency": PolicyUrgency.HIGH,
            "status": PolicyStatus.PUBLISHED,
            "policy_number": "MOEA-2024-002",
            "effective_date": datetime(2024, 4, 15),
            "impact_score": 85,
            "affected_industries": json.dumps(["半导体制造", "材料供应", "设备制造", "封装测试"]),
            "source_url": "https://www.moea.gov.tw/",
            "source_name": "经济部门",
            "tags": json.dumps(["供应链安全", "产业韧性", "自主可控"]),
            "keywords": "供应链,韧性,战略储备,风险监测"
        }
    ]
    
    # 创建政策数据
    for policy_data in policies_data:
        policy = Policy(
            **policy_data,
            created_by=admin_user.id
        )
        db.add(policy)
    
    db.commit()
    print(f"✅ 创建了 {len(policies_data)} 条政策数据")

def main():
    """主函数"""
    print("开始初始化数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建admin用户
        admin_user = create_admin_user(db)
        
        # 创建政策数据
        create_policy_data(db, admin_user)
        
        print("✅ 数据初始化完成！")
        print("Admin账号信息：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("  邮箱: admin@semix.com")
        
    except Exception as e:
        print(f"❌ 数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
