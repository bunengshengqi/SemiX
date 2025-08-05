#!/usr/bin/env python3
"""
市场情报数据初始化脚本 - 创建50条市场情报数据
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
from app.models.market_intelligence import (
    MarketIntelligence, IntelligenceType, IntelligencePriority, 
    IntelligenceStatus, MarketRegion
)

def create_market_intelligence_data(db: Session):
    """创建50条市场情报数据"""
    
    # 检查是否已有市场情报数据
    existing_intelligence = db.query(MarketIntelligence).count()
    if existing_intelligence > 0:
        print(f"已存在 {existing_intelligence} 条市场情报数据")
        return
    
    # 获取admin用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        print("❌ 未找到admin用户，请先运行 init_db.py")
        return
    
    # 市场情报数据
    intelligence_data = [
        # 市场趋势类情报 (15条)
        {
            "title": "2024年全球半导体市场规模预计达到6740亿美元",
            "subtitle": "AI芯片需求推动市场强劲增长",
            "summary": "根据最新市场研究报告，2024年全球半导体市场规模预计将达到6740亿美元，同比增长13.1%。人工智能芯片需求的爆发式增长是主要驱动因素。",
            "content": "详细分析显示，AI芯片市场预计将在2024年增长50%以上，达到710亿美元。数据中心GPU、AI推理芯片和边缘AI处理器是增长最快的细分市场。NVIDIA、AMD、Intel等主要厂商都在加大AI芯片投资。同时，汽车半导体、物联网芯片等传统市场也保持稳定增长。预计2025年市场将继续保持两位数增长。",
            "intelligence_type": IntelligenceType.MARKET_TREND,
            "priority": IntelligencePriority.HIGH,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.GLOBAL,
            "industry_sectors": json.dumps(["半导体", "人工智能", "数据中心"]),
            "product_categories": json.dumps(["AI芯片", "GPU", "处理器"]),
            "market_size": 6740.0,
            "growth_rate": 13.1,
            "report_date": datetime.now() - timedelta(days=1),
            "data_period_start": datetime(2024, 1, 1),
            "data_period_end": datetime(2024, 12, 31),
            "data_sources": json.dumps(["Gartner", "IDC", "SEMI"]),
            "author": "张明华",
            "organization": "半导体产业研究院",
            "tags": json.dumps(["半导体", "AI芯片", "市场预测", "增长"]),
            "keywords": "半导体,AI芯片,市场规模,增长预测",
            "quality_score": 4.8,
            "relevance_score": 4.9,
            "timeliness_score": 4.7,
            "is_featured": True,
            "is_trending": True,
            "is_verified": True,
            "view_count": 1250,
            "like_count": 89,
            "share_count": 34,
            "comment_count": 12,
            "created_by": admin_user.id
        },
        {
            "title": "中国大陆晶圆代工产能将在2025年超越台湾省",
            "subtitle": "本土化进程加速，产业格局重塑",
            "summary": "最新产业分析显示，中国大陆晶圆代工产能预计将在2025年首次超越台湾省，成为全球最大的晶圆代工基地。",
            "content": "中芯国际、华虹集团等大陆晶圆代工厂商正在大规模扩产，预计2025年大陆晶圆代工产能将达到每月1200万片8英寸等效晶圆。同时，台积电、联电等台湾省厂商也在大陆设厂。这一变化将重塑全球半导体产业格局，对供应链安全和成本结构产生深远影响。",
            "intelligence_type": IntelligenceType.MARKET_TREND,
            "priority": IntelligencePriority.CRITICAL,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.ASIA_PACIFIC,
            "industry_sectors": json.dumps(["晶圆代工", "半导体制造"]),
            "product_categories": json.dumps(["晶圆", "芯片制造"]),
            "market_share": 35.2,
            "growth_rate": 28.5,
            "report_date": datetime.now() - timedelta(days=2),
            "author": "李晓东",
            "organization": "中国半导体行业协会",
            "tags": json.dumps(["晶圆代工", "产能", "中国大陆", "台湾省"]),
            "keywords": "晶圆代工,产能,中芯国际,台积电",
            "quality_score": 4.6,
            "relevance_score": 4.8,
            "timeliness_score": 4.9,
            "is_featured": True,
            "is_trending": True,
            "is_verified": True,
            "view_count": 980,
            "like_count": 67,
            "share_count": 28,
            "comment_count": 15,
            "created_by": admin_user.id
        },
        
        # 价格分析类情报 (10条)
        {
            "title": "存储芯片价格触底反弹，DRAM价格环比上涨15%",
            "subtitle": "库存去化完成，需求回暖推动价格上涨",
            "summary": "经过长达18个月的价格下跌后，存储芯片价格终于触底反弹。11月DRAM价格环比上涨15%，NAND Flash价格上涨8%。",
            "content": "存储芯片价格反弹主要受以下因素推动：1）库存去化基本完成，渠道库存降至健康水平；2）AI服务器需求带动高容量DRAM需求增长；3）智能手机市场回暖，带动移动存储需求；4）主要厂商减产效果显现。预计价格上涨趋势将持续到2024年Q2。",
            "intelligence_type": IntelligenceType.PRICE_ANALYSIS,
            "priority": IntelligencePriority.HIGH,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.GLOBAL,
            "industry_sectors": json.dumps(["存储芯片", "DRAM", "NAND Flash"]),
            "product_categories": json.dumps(["存储器", "内存", "闪存"]),
            "price_change": 15.0,
            "growth_rate": 12.3,
            "report_date": datetime.now() - timedelta(days=3),
            "author": "王芳",
            "organization": "DRAMeXchange",
            "tags": json.dumps(["存储芯片", "价格", "DRAM", "反弹"]),
            "keywords": "存储芯片,DRAM,价格,上涨,反弹",
            "quality_score": 4.5,
            "relevance_score": 4.7,
            "timeliness_score": 4.8,
            "is_featured": False,
            "is_trending": True,
            "is_verified": True,
            "view_count": 756,
            "like_count": 45,
            "share_count": 19,
            "comment_count": 8,
            "created_by": admin_user.id
        },
        
        # 供应链情报 (8条)
        {
            "title": "台积电3nm工艺良率提升至70%，苹果A18芯片量产顺利",
            "subtitle": "先进制程技术突破，为下一代iPhone铺路",
            "summary": "台积电3nm工艺制程良率已提升至70%，达到量产标准。苹果A18芯片正在台积电3nm产线上顺利量产，为iPhone 16系列做准备。",
            "content": "台积电N3E工艺节点在经过一年多的优化后，良率从初期的55%提升至目前的70%。这一突破使得3nm芯片的成本大幅下降，为大规模商用奠定基础。苹果A18芯片采用3nm工艺，集成了更强大的AI处理单元，性能相比A17提升20%，功耗降低15%。预计iPhone 16系列将在明年9月发布。",
            "intelligence_type": IntelligenceType.SUPPLY_CHAIN,
            "priority": IntelligencePriority.HIGH,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.ASIA_PACIFIC,
            "industry_sectors": json.dumps(["晶圆代工", "移动处理器"]),
            "product_categories": json.dumps(["3nm芯片", "手机处理器"]),
            "report_date": datetime.now() - timedelta(days=4),
            "author": "陈志强",
            "organization": "DigiTimes",
            "tags": json.dumps(["台积电", "3nm", "苹果", "A18", "良率"]),
            "keywords": "台积电,3nm,苹果,A18,良率,量产",
            "quality_score": 4.7,
            "relevance_score": 4.6,
            "timeliness_score": 4.8,
            "is_featured": True,
            "is_trending": False,
            "is_verified": True,
            "view_count": 892,
            "like_count": 56,
            "share_count": 23,
            "comment_count": 11,
            "created_by": admin_user.id
        },
        
        # 技术趋势类情报 (7条)
        {
            "title": "Chiplet技术成为半导体行业新趋势，AMD、Intel积极布局",
            "subtitle": "模块化设计降低成本，提升良率和灵活性",
            "summary": "Chiplet（芯粒）技术正成为半导体行业的新趋势。通过将大芯片拆分为多个小芯片，可以显著提升良率、降低成本，并提供更大的设计灵活性。",
            "content": "Chiplet技术的核心优势包括：1）提升良率：小芯片良率远高于大芯片；2）降低成本：可以使用不同工艺节点制造不同功能模块；3）提升灵活性：可以根据需求组合不同功能模块；4）加速上市时间：可以重用已验证的IP模块。AMD的EPYC和Ryzen处理器已大规模采用Chiplet设计，Intel的Meteor Lake也采用了类似架构。",
            "intelligence_type": IntelligenceType.TECHNOLOGY_TREND,
            "priority": IntelligencePriority.MEDIUM,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.GLOBAL,
            "industry_sectors": json.dumps(["处理器设计", "封装技术"]),
            "product_categories": json.dumps(["CPU", "GPU", "SoC"]),
            "report_date": datetime.now() - timedelta(days=5),
            "author": "刘建国",
            "organization": "IEEE Spectrum",
            "tags": json.dumps(["Chiplet", "芯粒", "AMD", "Intel", "技术趋势"]),
            "keywords": "Chiplet,芯粒,模块化,AMD,Intel,处理器",
            "quality_score": 4.4,
            "relevance_score": 4.5,
            "timeliness_score": 4.3,
            "is_featured": False,
            "is_trending": False,
            "is_verified": True,
            "view_count": 634,
            "like_count": 38,
            "share_count": 15,
            "comment_count": 6,
            "created_by": admin_user.id
        },
        
        # 竞争对手分析 (5条)
        {
            "title": "NVIDIA在AI芯片市场份额达到80%，竞争对手奋起直追",
            "subtitle": "AMD、Intel、谷歌等厂商加大AI芯片投入",
            "summary": "NVIDIA凭借其GPU在AI训练和推理市场的优势，目前占据约80%的AI芯片市场份额。但AMD、Intel、谷歌等竞争对手正在加大投入，试图打破NVIDIA的垄断地位。",
            "content": "NVIDIA的优势主要来自：1）CUDA生态系统的先发优势；2）H100、A100等产品的强大性能；3）完整的软硬件解决方案。竞争对手的应对策略：AMD推出MI300系列与H100竞争；Intel发布Gaudi3 AI芯片；谷歌TPU专注自用；中国厂商如寒武纪、海光等也在加大投入。预计2025年NVIDIA市场份额将下降至70%左右。",
            "intelligence_type": IntelligenceType.COMPETITOR_ANALYSIS,
            "priority": IntelligencePriority.HIGH,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.GLOBAL,
            "industry_sectors": json.dumps(["AI芯片", "GPU", "数据中心"]),
            "product_categories": json.dumps(["AI训练芯片", "AI推理芯片"]),
            "market_share": 80.0,
            "report_date": datetime.now() - timedelta(days=6),
            "author": "赵敏",
            "organization": "Jon Peddie Research",
            "tags": json.dumps(["NVIDIA", "AI芯片", "竞争", "市场份额"]),
            "keywords": "NVIDIA,AI芯片,GPU,竞争,市场份额",
            "quality_score": 4.6,
            "relevance_score": 4.8,
            "timeliness_score": 4.5,
            "is_featured": True,
            "is_trending": True,
            "is_verified": True,
            "view_count": 1123,
            "like_count": 78,
            "share_count": 31,
            "comment_count": 19,
            "created_by": admin_user.id
        },
        
        # 行业新闻 (3条)
        {
            "title": "三星电子宣布投资170亿美元在德州建设新晶圆厂",
            "subtitle": "加强美国本土半导体制造能力",
            "summary": "三星电子宣布将投资170亿美元在德克萨斯州泰勒市建设新的晶圆制造工厂，预计2026年开始量产，主要生产先进制程芯片。",
            "content": "这座新工厂将是三星在美国的第二座晶圆厂，采用4nm和3nm先进制程技术，月产能预计达到10万片12英寸晶圆。工厂将为美国本土客户提供服务，包括高通、英伟达等芯片设计公司。此举是三星响应美国《芯片法案》的重要举措，也是其全球化布局的重要一步。",
            "intelligence_type": IntelligenceType.INDUSTRY_NEWS,
            "priority": IntelligencePriority.MEDIUM,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.NORTH_AMERICA,
            "industry_sectors": json.dumps(["晶圆制造", "半导体投资"]),
            "product_categories": json.dumps(["先进制程芯片"]),
            "report_date": datetime.now() - timedelta(days=7),
            "author": "孙丽华",
            "organization": "路透社",
            "tags": json.dumps(["三星", "投资", "美国", "晶圆厂"]),
            "keywords": "三星,投资,美国,晶圆厂,德州",
            "quality_score": 4.2,
            "relevance_score": 4.3,
            "timeliness_score": 4.6,
            "is_featured": False,
            "is_trending": False,
            "is_verified": True,
            "view_count": 567,
            "like_count": 32,
            "share_count": 12,
            "comment_count": 5,
            "created_by": admin_user.id
        },
        
        # 政策影响 (2条)
        {
            "title": "美国更新对华半导体出口管制清单，影响AI芯片贸易",
            "subtitle": "新规定将于2024年1月生效，涉及更多AI相关技术",
            "summary": "美国商务部发布最新对华半导体出口管制规定，进一步限制AI芯片和相关技术的出口，新规定将于2024年1月1日生效。",
            "content": "新规定主要变化包括：1）扩大AI芯片管制范围，包括算力超过一定阈值的芯片；2）加强对半导体制造设备的管制；3）限制美国人员为中国半导体企业提供技术服务；4）要求获得许可证才能向中国出口相关产品。这将对中美半导体贸易产生重大影响，中国企业需要寻找替代方案。",
            "intelligence_type": IntelligenceType.POLICY_IMPACT,
            "priority": IntelligencePriority.CRITICAL,
            "status": IntelligenceStatus.PUBLISHED,
            "region": MarketRegion.GLOBAL,
            "industry_sectors": json.dumps(["半导体贸易", "AI芯片", "出口管制"]),
            "product_categories": json.dumps(["AI芯片", "半导体设备"]),
            "report_date": datetime.now() - timedelta(days=8),
            "author": "马晓峰",
            "organization": "华尔街日报",
            "tags": json.dumps(["出口管制", "AI芯片", "中美贸易", "政策"]),
            "keywords": "出口管制,AI芯片,中美贸易,政策影响",
            "quality_score": 4.7,
            "relevance_score": 4.9,
            "timeliness_score": 4.8,
            "is_featured": True,
            "is_trending": True,
            "is_verified": True,
            "view_count": 1456,
            "like_count": 95,
            "share_count": 42,
            "comment_count": 28,
            "created_by": admin_user.id
        }
    ]
    
    # 生成更多随机数据以达到50条
    additional_data = generate_additional_intelligence(admin_user.id, len(intelligence_data))
    intelligence_data.extend(additional_data)
    
    print(f"准备创建 {len(intelligence_data)} 条市场情报数据...")
    
    # 批量创建市场情报
    for intel_data in intelligence_data:
        intelligence = MarketIntelligence(**intel_data)
        db.add(intelligence)
    
    db.commit()
    print(f"✅ 创建了 {len(intelligence_data)} 条市场情报数据")

def generate_additional_intelligence(admin_user_id: int, existing_count: int):
    """生成额外的市场情报数据，总共达到50条"""
    
    additional_data = []
    
    # 模板数据用于生成随机情报
    templates = [
        {
            "title_template": "{}市场{}季度增长{}%，预计全年达到{}亿美元",
            "type": IntelligenceType.MARKET_TREND,
            "regions": [MarketRegion.CHINA, MarketRegion.JAPAN, MarketRegion.SOUTH_KOREA],
            "sectors": ["存储芯片", "处理器", "传感器", "功率半导体", "模拟芯片"]
        },
        {
            "title_template": "{}价格{}月环比{}{}%，供需关系发生变化",
            "type": IntelligenceType.PRICE_ANALYSIS,
            "regions": [MarketRegion.GLOBAL, MarketRegion.ASIA_PACIFIC],
            "sectors": ["DRAM", "NAND Flash", "CPU", "GPU", "MCU"]
        },
        {
            "title_template": "{}公司发布{}技术，性能提升{}%",
            "type": IntelligenceType.TECHNOLOGY_TREND,
            "regions": [MarketRegion.GLOBAL],
            "sectors": ["AI芯片", "5G芯片", "汽车芯片", "物联网芯片"]
        }
    ]
    
    companies = ["英特尔", "AMD", "高通", "博通", "联发科", "海思", "紫光展锐", "兆易创新"]
    authors = ["李明", "张华", "王强", "刘芳", "陈杰", "赵敏", "孙丽", "周涛"]
    organizations = ["半导体研究院", "市场分析公司", "行业协会", "咨询机构", "研究中心"]
    
    # 生成剩余数据
    for i in range(existing_count, 50):
        template = random.choice(templates)
        
        # 生成随机标题
        if template["type"] == IntelligenceType.MARKET_TREND:
            title = template["title_template"].format(
                random.choice(template["sectors"]),
                random.choice(["第一", "第二", "第三", "第四"]),
                random.randint(5, 25),
                random.randint(100, 2000)
            )
        elif template["type"] == IntelligenceType.PRICE_ANALYSIS:
            title = template["title_template"].format(
                random.choice(template["sectors"]),
                random.randint(1, 12),
                random.choice(["上涨", "下跌"]),
                random.randint(3, 20)
            )
        else:
            title = template["title_template"].format(
                random.choice(companies),
                random.choice(["新一代", "革命性", "突破性"]),
                random.randint(10, 50)
            )
        
        intel_data = {
            "title": title,
            "subtitle": f"行业分析报告第{i+1}期",
            "summary": f"这是第{i+1}条市场情报的摘要信息，包含了重要的市场动态和趋势分析。",
            "content": f"详细内容：{title}。本报告深入分析了相关市场动态，提供了专业的见解和预测。通过对行业数据的深入挖掘，我们发现了一些重要的趋势和机会。这些信息对于行业从业者和投资者具有重要的参考价值。",
            "intelligence_type": template["type"],
            "priority": random.choice(list(IntelligencePriority)),
            "status": IntelligenceStatus.PUBLISHED,
            "region": random.choice(template["regions"]),
            "industry_sectors": json.dumps(random.sample(template["sectors"], min(2, len(template["sectors"])))),
            "product_categories": json.dumps([f"产品类别{j+1}" for j in range(2)]),
            "market_size": round(random.uniform(50, 1000), 1) if random.choice([True, False]) else None,
            "growth_rate": round(random.uniform(-10, 30), 1) if random.choice([True, False]) else None,
            "market_share": round(random.uniform(5, 50), 1) if random.choice([True, False]) else None,
            "price_change": round(random.uniform(-20, 20), 1) if template["type"] == IntelligenceType.PRICE_ANALYSIS else None,
            "report_date": datetime.now() - timedelta(days=random.randint(1, 30)),
            "data_period_start": datetime.now() - timedelta(days=random.randint(90, 365)),
            "data_period_end": datetime.now() - timedelta(days=random.randint(1, 90)),
            "data_sources": json.dumps(random.sample(["Gartner", "IDC", "SEMI", "IC Insights", "Omdia"], 2)),
            "author": random.choice(authors),
            "organization": random.choice(organizations),
            "tags": json.dumps([f"标签{j+1}" for j in range(3)]),
            "keywords": f"关键词{i+1},市场,分析,趋势",
            "quality_score": round(random.uniform(3.5, 5.0), 1),
            "relevance_score": round(random.uniform(3.5, 5.0), 1),
            "timeliness_score": round(random.uniform(3.5, 5.0), 1),
            "is_featured": random.choice([True, False]),
            "is_trending": random.choice([True, False]),
            "is_premium": random.choice([True, False]),
            "is_verified": True,
            "view_count": random.randint(50, 1000),
            "like_count": random.randint(5, 100),
            "share_count": random.randint(1, 50),
            "comment_count": random.randint(0, 20),
            "created_by": admin_user_id
        }
        
        additional_data.append(intel_data)
    
    return additional_data

def main():
    """主函数"""
    print("🚀 开始初始化市场情报数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建市场情报数据
        create_market_intelligence_data(db)
        
        print("✅ 市场情报数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 市场情报数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
