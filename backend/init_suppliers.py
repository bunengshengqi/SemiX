#!/usr/bin/env python3
"""
供应商数据初始化脚本 - 创建50条供应商数据
"""
import os
import sys
from datetime import datetime
import json
import random

# 设置环境变量使用SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./semix.db'

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.models.user import User
from app.models.supplier import Supplier, SupplierType, SupplierScale, CertificationLevel

def generate_additional_suppliers(admin_user_id: int):
    """生成额外的供应商数据，总共达到50条"""

    # 台湾省供应商数据
    taiwan_suppliers = [
        {
            "company_name": "台积电材料科技股份有限公司",
            "company_name_en": "TSMC Materials Technology Co., Ltd.",
            "brand_name": "TMT",
            "contact_person": "陈志明",
            "email": "info@tmt-taiwan.com",
            "phone": "+886-3-1234-5678",
            "website": "https://www.tmt-taiwan.com",
            "country": "台湾省",
            "province": "新竹县",
            "city": "新竹",
            "address": "新竹科学园区力行路1号",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.LARGE,
            "established_year": 1987,
            "employee_count": 4500,
            "annual_revenue": 25000.0,
            "main_products": json.dumps(["先进制程芯片", "逻辑芯片", "专用芯片"]),
            "product_categories": json.dumps(["半导体制造", "晶圆代工"]),
            "service_scope": "晶圆代工、封装测试、技术服务",
            "technology_level": "世界领先",
            "certifications": json.dumps(["ISO9001", "ISO14001", "IATF16949", "ISO45001"]),
            "patents_count": 456,
            "certification_level": CertificationLevel.PREMIUM,
            "quality_certifications": json.dumps(["ISO9001:2015", "ISO14001:2015"]),
            "overall_rating": 4.9,
            "quality_rating": 5.0,
            "service_rating": 4.8,
            "delivery_rating": 4.9,
            "price_rating": 4.7,
            "review_count": 234,
            "min_order_quantity": "10000pcs",
            "payment_terms": "T/T 30天",
            "delivery_time": "6-8周",
            "export_countries": json.dumps(["全球"]),
            "major_clients": json.dumps(["Apple", "NVIDIA", "AMD", "Qualcomm"]),
            "partnerships": json.dumps(["ASML", "Applied Materials"]),
            "exhibitions": json.dumps(["SEMICON Taiwan", "Computex"]),
            "awards": json.dumps(["全球半导体制造领导者奖", "技术创新大奖2023"]),
            "company_description": "全球领先的半导体制造服务公司，在先进制程技术方面处于世界前列。",
            "competitive_advantages": "先进制程技术、全球服务网络、技术创新能力",
            "tags": json.dumps(["晶圆代工", "先进制程", "台湾制造", "全球领先"]),
            "keywords": "晶圆代工,先进制程,逻辑芯片,专用芯片",
            "is_active": True,
            "is_featured": True,
            "is_verified": True,
            "created_by": admin_user_id
        }
    ]

    # 东南亚供应商数据
    sea_suppliers = [
        {
            "company_name": "新加坡先进封装技术有限公司",
            "company_name_en": "Singapore Advanced Packaging Technology Pte Ltd",
            "brand_name": "SAPT",
            "contact_person": "Lim Wei Ming",
            "email": "info@sapt.com.sg",
            "phone": "+65-6123-4567",
            "website": "https://www.sapt.com.sg",
            "country": "东南亚",
            "province": "新加坡",
            "city": "新加坡",
            "address": "2 Science Park Drive, Singapore 118222",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.LARGE,
            "established_year": 1998,
            "employee_count": 1800,
            "annual_revenue": 8500.0,
            "main_products": json.dumps(["先进封装", "系统级封装", "芯片测试"]),
            "product_categories": json.dumps(["封装测试", "系统集成"]),
            "service_scope": "封装设计、制造、测试、物流",
            "technology_level": "先进封装",
            "certifications": json.dumps(["ISO9001", "ISO14001", "IATF16949"]),
            "patents_count": 89,
            "certification_level": CertificationLevel.PREMIUM,
            "quality_certifications": json.dumps(["ISO9001:2015", "ISO14001:2015"]),
            "overall_rating": 4.6,
            "quality_rating": 4.7,
            "service_rating": 4.5,
            "delivery_rating": 4.6,
            "price_rating": 4.4,
            "review_count": 112,
            "min_order_quantity": "1000pcs",
            "payment_terms": "T/T 30天",
            "delivery_time": "4-6周",
            "export_countries": json.dumps(["中国", "日本", "韩国", "美国", "欧洲"]),
            "major_clients": json.dumps(["Broadcom", "MediaTek", "Infineon"]),
            "partnerships": json.dumps(["ASE Group", "Amkor"]),
            "exhibitions": json.dumps(["SEMICON Southeast Asia", "Electronica Asia"]),
            "awards": json.dumps(["新加坡制造业卓越奖", "封装技术创新奖2022"]),
            "company_description": "专业的半导体封装测试服务提供商，在先进封装技术方面具有领先优势。",
            "competitive_advantages": "先进封装技术、快速响应、全球服务",
            "tags": json.dumps(["先进封装", "系统级封装", "新加坡制造"]),
            "keywords": "先进封装,系统级封装,芯片测试,SiP",
            "is_active": True,
            "is_featured": True,
            "is_verified": True,
            "created_by": admin_user_id
        }
    ]

    # 生成更多随机供应商数据以达到50条
    countries = ["日本", "韩国", "台湾省", "东南亚"]
    company_types = ["半导体", "电子", "科技", "材料", "设备"]

    random_suppliers = []
    for i in range(46):  # 已有4条，再生成46条达到50条
        country = random.choice(countries)
        company_type = random.choice(company_types)

        supplier = {
            "company_name": f"{country}{company_type}有限公司{i+1:02d}",
            "company_name_en": f"{country} {company_type} Co., Ltd. {i+1:02d}",
            "brand_name": f"{company_type[:2].upper()}{i+1:02d}",
            "contact_person": f"联系人{i+1:02d}",
            "email": f"contact{i+1:02d}@{company_type.lower()}.com",
            "phone": f"+{random.randint(81, 886)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "website": f"https://www.{company_type.lower()}{i+1:02d}.com",
            "country": country,
            "province": f"{country}省" if country != "东南亚" else random.choice(["新加坡", "马来西亚", "泰国"]),
            "city": f"{country}市",
            "address": f"{country}市工业区{i+1}号",
            "supplier_type": random.choice(list(SupplierType)),
            "scale": random.choice(list(SupplierScale)),
            "established_year": random.randint(1980, 2020),
            "employee_count": random.randint(50, 5000),
            "annual_revenue": round(random.uniform(100, 20000), 1),
            "main_products": json.dumps([f"产品A{i+1}", f"产品B{i+1}", f"产品C{i+1}"]),
            "product_categories": json.dumps([f"类别{i%5+1}", f"类别{(i+1)%5+1}"]),
            "service_scope": "研发、生产、销售、服务",
            "technology_level": random.choice(["基础", "中等", "先进", "领先"]),
            "certifications": json.dumps(["ISO9001", "ISO14001"]),
            "patents_count": random.randint(0, 200),
            "certification_level": random.choice(list(CertificationLevel)),
            "quality_certifications": json.dumps(["ISO9001:2015"]),
            "overall_rating": round(random.uniform(3.0, 5.0), 1),
            "quality_rating": round(random.uniform(3.0, 5.0), 1),
            "service_rating": round(random.uniform(3.0, 5.0), 1),
            "delivery_rating": round(random.uniform(3.0, 5.0), 1),
            "price_rating": round(random.uniform(3.0, 5.0), 1),
            "review_count": random.randint(5, 200),
            "min_order_quantity": f"{random.randint(100, 10000)}pcs",
            "payment_terms": f"T/T {random.choice([30, 45, 60])}天",
            "delivery_time": f"{random.randint(2, 12)}周",
            "export_countries": json.dumps(random.sample(["中国", "美国", "欧洲", "日本", "韩国"], 3)),
            "major_clients": json.dumps([f"客户{j+1}" for j in range(3)]),
            "partnerships": json.dumps([f"合作伙伴{j+1}" for j in range(2)]),
            "exhibitions": json.dumps([f"展会{j+1}" for j in range(2)]),
            "awards": json.dumps([f"奖项{j+1}" for j in range(1)]),
            "company_description": f"专业的{company_type}企业，致力于为客户提供优质的产品和服务。",
            "competitive_advantages": "技术先进、质量可靠、服务优质",
            "tags": json.dumps([company_type, country, "专业"]),
            "keywords": f"{company_type},专业,优质,{country}",
            "is_active": True,
            "is_featured": random.choice([True, False]),
            "is_verified": random.choice([True, False]),
            "created_by": admin_user_id
        }
        random_suppliers.append(supplier)

    return taiwan_suppliers + sea_suppliers + random_suppliers

def create_supplier_data(db: Session):
    """创建50条供应商数据"""
    
    # 检查是否已有供应商数据
    existing_suppliers = db.query(Supplier).count()
    if existing_suppliers > 0:
        print(f"已存在 {existing_suppliers} 条供应商数据")
        return
    
    # 获取admin用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        print("❌ 未找到admin用户，请先运行 init_db.py")
        return
    
    # 供应商数据
    suppliers_data = [
        # 日本供应商 (12条)
        {
            "company_name": "东京半导体技术株式会社",
            "company_name_en": "Tokyo Semiconductor Technology Co., Ltd.",
            "brand_name": "TST",
            "contact_person": "田中太郎",
            "email": "info@tst-semi.co.jp",
            "phone": "+81-3-1234-5678",
            "website": "https://www.tst-semi.co.jp",
            "country": "日本",
            "province": "东京都",
            "city": "东京",
            "address": "东京都港区芝浦1-2-3",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.LARGE,
            "established_year": 1985,
            "employee_count": 2500,
            "annual_revenue": 15000.0,
            "main_products": json.dumps(["存储芯片", "处理器", "传感器"]),
            "product_categories": json.dumps(["半导体器件", "集成电路", "传感器"]),
            "service_scope": "设计、制造、测试、销售",
            "technology_level": "先进制程",
            "certifications": json.dumps(["ISO9001", "ISO14001", "IATF16949"]),
            "patents_count": 156,
            "certification_level": CertificationLevel.PREMIUM,
            "quality_certifications": json.dumps(["ISO9001:2015", "ISO14001:2015"]),
            "overall_rating": 4.8,
            "quality_rating": 4.9,
            "service_rating": 4.7,
            "delivery_rating": 4.8,
            "price_rating": 4.6,
            "review_count": 128,
            "min_order_quantity": "1000pcs",
            "payment_terms": "T/T 30天",
            "delivery_time": "4-6周",
            "export_countries": json.dumps(["中国", "韩国", "台湾省", "美国", "欧洲"]),
            "major_clients": json.dumps(["Sony", "Panasonic", "Nintendo"]),
            "partnerships": json.dumps(["TSMC", "Samsung"]),
            "exhibitions": json.dumps(["SEMICON Japan", "CEATEC"]),
            "awards": json.dumps(["日本半导体大奖2023", "技术创新奖"]),
            "company_description": "专业从事半导体器件研发制造的高科技企业，在存储芯片领域具有领先技术。",
            "competitive_advantages": "先进制程技术、高品质产品、快速响应",
            "tags": json.dumps(["半导体", "存储芯片", "日本制造", "高品质"]),
            "keywords": "半导体,存储芯片,处理器,传感器,日本",
            "is_active": True,
            "is_featured": True,
            "is_verified": True,
            "created_by": admin_user.id
        },
        {
            "company_name": "大阪电子材料有限公司",
            "company_name_en": "Osaka Electronic Materials Ltd.",
            "brand_name": "OEM",
            "contact_person": "佐藤花子",
            "email": "contact@oem-japan.com",
            "phone": "+81-6-9876-5432",
            "website": "https://www.oem-japan.com",
            "country": "日本",
            "province": "大阪府",
            "city": "大阪",
            "address": "大阪府大阪市北区梅田2-4-9",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.MEDIUM,
            "established_year": 1992,
            "employee_count": 800,
            "annual_revenue": 5200.0,
            "main_products": json.dumps(["光刻胶", "电子气体", "清洗剂"]),
            "product_categories": json.dumps(["半导体材料", "化学材料"]),
            "service_scope": "研发、生产、技术支持",
            "technology_level": "高端材料",
            "certifications": json.dumps(["ISO9001", "ISO14001"]),
            "patents_count": 89,
            "certification_level": CertificationLevel.VERIFIED,
            "quality_certifications": json.dumps(["ISO9001:2015"]),
            "overall_rating": 4.5,
            "quality_rating": 4.6,
            "service_rating": 4.4,
            "delivery_rating": 4.5,
            "price_rating": 4.3,
            "review_count": 76,
            "min_order_quantity": "50kg",
            "payment_terms": "T/T 45天",
            "delivery_time": "2-3周",
            "export_countries": json.dumps(["中国", "韩国", "台湾省"]),
            "major_clients": json.dumps(["Shin-Etsu", "JSR Corporation"]),
            "partnerships": json.dumps(["Tokyo Ohka Kogyo"]),
            "exhibitions": json.dumps(["SEMICON Japan", "NEPCON Japan"]),
            "awards": json.dumps(["材料创新奖2022"]),
            "company_description": "专业的半导体材料供应商，在光刻胶和电子气体领域有深厚技术积累。",
            "competitive_advantages": "高纯度材料、稳定供应、技术服务",
            "tags": json.dumps(["半导体材料", "光刻胶", "电子气体", "日本品质"]),
            "keywords": "半导体材料,光刻胶,电子气体,清洗剂",
            "is_active": True,
            "is_featured": False,
            "is_verified": True,
            "created_by": admin_user.id
        },
        # 继续添加更多日本供应商...
        {
            "company_name": "京都精密设备制造株式会社",
            "company_name_en": "Kyoto Precision Equipment Manufacturing Co.",
            "brand_name": "KPEM",
            "contact_person": "山田一郎",
            "email": "sales@kpem.co.jp",
            "phone": "+81-75-1111-2222",
            "website": "https://www.kpem.co.jp",
            "country": "日本",
            "province": "京都府",
            "city": "京都",
            "address": "京都府京都市下京区烏丸通七条下ル",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.MEDIUM,
            "established_year": 1988,
            "employee_count": 650,
            "annual_revenue": 4800.0,
            "main_products": json.dumps(["测试设备", "检测仪器", "自动化设备"]),
            "product_categories": json.dumps(["半导体设备", "测试设备"]),
            "service_scope": "设备制造、维护、技术培训",
            "technology_level": "精密制造",
            "certifications": json.dumps(["ISO9001", "CE"]),
            "patents_count": 45,
            "certification_level": CertificationLevel.VERIFIED,
            "quality_certifications": json.dumps(["ISO9001:2015"]),
            "overall_rating": 4.3,
            "quality_rating": 4.4,
            "service_rating": 4.2,
            "delivery_rating": 4.3,
            "price_rating": 4.1,
            "review_count": 52,
            "min_order_quantity": "1台",
            "payment_terms": "T/T 60天",
            "delivery_time": "8-12周",
            "export_countries": json.dumps(["中国", "东南亚"]),
            "major_clients": json.dumps(["Rohm", "Murata"]),
            "partnerships": json.dumps(["Advantest"]),
            "exhibitions": json.dumps(["SEMICON Japan"]),
            "awards": json.dumps(["精密制造奖2021"]),
            "company_description": "专业的半导体测试设备制造商，以精密制造和可靠性著称。",
            "competitive_advantages": "精密制造、可靠性高、服务完善",
            "tags": json.dumps(["测试设备", "精密制造", "日本工艺"]),
            "keywords": "测试设备,检测仪器,自动化设备,精密制造",
            "is_active": True,
            "is_featured": False,
            "is_verified": True,
            "created_by": admin_user.id
        },
        
        # 韩国供应商 (12条)
        {
            "company_name": "首尔半导体株式会社",
            "company_name_en": "Seoul Semiconductor Corporation",
            "brand_name": "SSC",
            "contact_person": "김민수",
            "email": "info@ssc-korea.com",
            "phone": "+82-2-1234-5678",
            "website": "https://www.ssc-korea.com",
            "country": "韩国",
            "province": "首尔特别市",
            "city": "首尔",
            "address": "首尔特别市江南区테헤란로 123",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.LARGE,
            "established_year": 1987,
            "employee_count": 3200,
            "annual_revenue": 18500.0,
            "main_products": json.dumps(["存储芯片", "系统芯片", "功率半导体"]),
            "product_categories": json.dumps(["半导体器件", "集成电路"]),
            "service_scope": "设计、制造、封装、测试",
            "technology_level": "先进制程",
            "certifications": json.dumps(["ISO9001", "ISO14001", "OHSAS18001"]),
            "patents_count": 234,
            "certification_level": CertificationLevel.PREMIUM,
            "quality_certifications": json.dumps(["ISO9001:2015", "ISO14001:2015"]),
            "overall_rating": 4.7,
            "quality_rating": 4.8,
            "service_rating": 4.6,
            "delivery_rating": 4.7,
            "price_rating": 4.5,
            "review_count": 156,
            "min_order_quantity": "5000pcs",
            "payment_terms": "T/T 30天",
            "delivery_time": "3-5周",
            "export_countries": json.dumps(["中国", "日本", "美国", "欧洲", "东南亚"]),
            "major_clients": json.dumps(["Samsung", "LG", "SK Hynix"]),
            "partnerships": json.dumps(["TSMC", "GlobalFoundries"]),
            "exhibitions": json.dumps(["SEMICON Korea", "K-DISPLAY"]),
            "awards": json.dumps(["韩国半导体大奖2023", "出口优秀企业奖"]),
            "company_description": "韩国领先的半导体制造企业，在存储和系统芯片领域具有强大实力。",
            "competitive_advantages": "先进技术、大规模生产、成本优势",
            "tags": json.dumps(["半导体", "存储芯片", "韩国制造", "大规模生产"]),
            "keywords": "半导体,存储芯片,系统芯片,功率半导体,韩国",
            "is_active": True,
            "is_featured": True,
            "is_verified": True,
            "created_by": admin_user.id
        },
        {
            "company_name": "釜山电子材料有限公司",
            "company_name_en": "Busan Electronic Materials Co., Ltd.",
            "brand_name": "BEM",
            "contact_person": "박지영",
            "email": "contact@bem-korea.com",
            "phone": "+82-51-9876-5432",
            "website": "https://www.bem-korea.com",
            "country": "韩国",
            "province": "釜山广域市",
            "city": "釜山",
            "address": "釜山广域市海云台区 센텀중앙로 79",
            "supplier_type": SupplierType.MANUFACTURER,
            "scale": SupplierScale.MEDIUM,
            "established_year": 1995,
            "employee_count": 920,
            "annual_revenue": 6800.0,
            "main_products": json.dumps(["硅晶圆", "化合物半导体", "封装材料"]),
            "product_categories": json.dumps(["半导体材料", "基板材料"]),
            "service_scope": "材料研发、生产、质量检测",
            "technology_level": "高端材料",
            "certifications": json.dumps(["ISO9001", "ISO14001"]),
            "patents_count": 67,
            "certification_level": CertificationLevel.VERIFIED,
            "quality_certifications": json.dumps(["ISO9001:2015"]),
            "overall_rating": 4.4,
            "quality_rating": 4.5,
            "service_rating": 4.3,
            "delivery_rating": 4.4,
            "price_rating": 4.2,
            "review_count": 89,
            "min_order_quantity": "100片",
            "payment_terms": "T/T 45天",
            "delivery_time": "3-4周",
            "export_countries": json.dumps(["中国", "日本", "台湾省"]),
            "major_clients": json.dumps(["SK Siltron", "LG Innotek"]),
            "partnerships": json.dumps(["Sumco", "Shin-Etsu"]),
            "exhibitions": json.dumps(["SEMICON Korea"]),
            "awards": json.dumps(["材料技术奖2022"]),
            "company_description": "专业的半导体材料供应商，在硅晶圆和化合物半导体领域有丰富经验。",
            "competitive_advantages": "高品质材料、稳定供应、技术创新",
            "tags": json.dumps(["半导体材料", "硅晶圆", "化合物半导体"]),
            "keywords": "硅晶圆,化合物半导体,封装材料,基板",
            "is_active": True,
            "is_featured": False,
            "is_verified": True,
            "created_by": admin_user.id
        }
    ]
    
    # 生成更多供应商数据
    additional_suppliers = generate_additional_suppliers(admin_user.id)
    suppliers_data.extend(additional_suppliers)

    print(f"准备创建 {len(suppliers_data)} 条供应商数据...")
    
    # 批量创建供应商
    for supplier_data in suppliers_data:
        supplier = Supplier(**supplier_data)
        db.add(supplier)
    
    db.commit()
    print(f"✅ 创建了 {len(suppliers_data)} 条供应商数据")

def main():
    """主函数"""
    print("开始初始化供应商数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建供应商数据
        create_supplier_data(db)
        
        print("✅ 供应商数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 供应商数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
