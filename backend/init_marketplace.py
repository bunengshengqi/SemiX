#!/usr/bin/env python3
"""
二手交易数据初始化脚本 - 创建交易信息数据
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
from app.models.marketplace import (
    MarketplaceListing, ListingType, ListingStatus, ProductCondition, PriceType
)

def create_marketplace_data(db: Session):
    """创建二手交易数据"""
    
    # 检查是否已有交易数据
    existing_listings = db.query(MarketplaceListing).count()
    if existing_listings > 0:
        print(f"已存在 {existing_listings} 条交易信息")
        return
    
    # 获取admin用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        print("❌ 未找到admin用户，请先运行 init_db.py")
        return
    
    # 交易信息数据
    listings_data = [
        # 出售信息 (20条)
        {
            "title": "全新未拆封 NVIDIA RTX 4090 显卡 急售",
            "description": "由于项目取消，现有全新未拆封的NVIDIA GeForce RTX 4090显卡一张，原价购入，现急需出售。包装完整，发票齐全，支持验货。",
            "listing_type": ListingType.SELL,
            "status": ListingStatus.ACTIVE,
            "product_name": "GeForce RTX 4090",
            "manufacturer": "NVIDIA",
            "model_number": "RTX 4090",
            "part_number": "RTX4090-24G",
            "category": "显卡",
            "subcategory": "游戏显卡",
            "specifications": json.dumps({
                "显存": "24GB GDDR6X",
                "核心频率": "2230 MHz",
                "显存频率": "21000 MHz",
                "接口": "PCIe 4.0 x16",
                "功耗": "450W"
            }),
            "quantity": 1,
            "condition": ProductCondition.NEW,
            "condition_notes": "全新未拆封，包装完整",
            "price": 1599.0,
            "currency": "USD",
            "price_type": PriceType.NEGOTIABLE,
            "total_value": 1599.0,
            "country": "中国",
            "state_province": "广东省",
            "city": "深圳市",
            "shipping_from": "深圳市南山区",
            "payment_terms": "支付宝、微信、银行转账",
            "shipping_terms": "顺丰包邮",
            "delivery_time": "1-2个工作日",
            "warranty_info": "原厂3年质保",
            "contact_name": "张先生",
            "contact_email": "zhang@example.com",
            "contact_phone": "+86-138-0000-1234",
            "company_name": "深圳科技有限公司",
            "images": json.dumps([
                "https://example.com/images/rtx4090_1.jpg",
                "https://example.com/images/rtx4090_2.jpg"
            ]),
            "expires_at": datetime.now() + timedelta(days=30),
            "tags": json.dumps(["显卡", "NVIDIA", "RTX4090", "全新", "急售"]),
            "keywords": "RTX4090,显卡,NVIDIA,全新,急售",
            "is_verified": True,
            "is_featured": True,
            "is_urgent": True,
            "view_count": 156,
            "inquiry_count": 8,
            "favorite_count": 12,
            "created_by": admin_user.id
        },
        {
            "title": "Intel Core i9-13900K 处理器 9成新",
            "description": "个人使用的Intel i9-13900K处理器，使用时间约6个月，性能完好，无超频使用历史。配原装散热器和包装盒。",
            "listing_type": ListingType.SELL,
            "status": ListingStatus.ACTIVE,
            "product_name": "Core i9-13900K",
            "manufacturer": "Intel",
            "model_number": "i9-13900K",
            "part_number": "BX8071513900K",
            "category": "处理器",
            "subcategory": "桌面处理器",
            "specifications": json.dumps({
                "核心数": "24核心(8P+16E)",
                "线程数": "32线程",
                "基础频率": "3.0 GHz",
                "最大睿频": "5.8 GHz",
                "缓存": "36MB",
                "接口": "LGA1700"
            }),
            "quantity": 1,
            "condition": ProductCondition.EXCELLENT,
            "condition_notes": "使用6个月，无超频，性能完好",
            "price": 450.0,
            "currency": "USD",
            "price_type": PriceType.FIXED,
            "total_value": 450.0,
            "country": "美国",
            "state_province": "加利福尼亚州",
            "city": "旧金山",
            "shipping_from": "San Francisco, CA",
            "payment_terms": "PayPal, Zelle",
            "shipping_terms": "USPS Priority Mail",
            "delivery_time": "2-3 business days",
            "warranty_info": "剩余2.5年Intel质保",
            "contact_name": "John Smith",
            "contact_email": "john.smith@example.com",
            "contact_phone": "+1-415-555-0123",
            "images": json.dumps([
                "https://example.com/images/i9_13900k_1.jpg"
            ]),
            "expires_at": datetime.now() + timedelta(days=45),
            "tags": json.dumps(["处理器", "Intel", "i9", "13900K"]),
            "keywords": "Intel,i9,13900K,处理器,CPU",
            "is_verified": True,
            "is_featured": False,
            "is_urgent": False,
            "view_count": 89,
            "inquiry_count": 5,
            "favorite_count": 7,
            "created_by": admin_user.id
        },
        {
            "title": "三星 32GB DDR5-4800 内存条 2根装",
            "description": "三星原厂DDR5内存，32GB容量，频率4800MHz，ECC纠错功能。服务器拆机件，测试正常，适合工作站使用。",
            "listing_type": ListingType.SELL,
            "status": ListingStatus.ACTIVE,
            "product_name": "DDR5-4800 32GB",
            "manufacturer": "Samsung",
            "model_number": "M393A4K40DB3-CWE",
            "part_number": "M393A4K40DB3-CWE",
            "category": "内存",
            "subcategory": "服务器内存",
            "specifications": json.dumps({
                "容量": "32GB",
                "类型": "DDR5",
                "频率": "4800MHz",
                "时序": "CL40",
                "电压": "1.1V",
                "ECC": "支持"
            }),
            "quantity": 2,
            "min_order_quantity": 1,
            "condition": ProductCondition.GOOD,
            "condition_notes": "服务器拆机，功能正常，外观有轻微使用痕迹",
            "price": 180.0,
            "currency": "USD",
            "price_type": PriceType.NEGOTIABLE,
            "total_value": 360.0,
            "country": "韩国",
            "state_province": "首尔特别市",
            "city": "首尔",
            "shipping_from": "Seoul, South Korea",
            "payment_terms": "银行转账、PayPal",
            "shipping_terms": "DHL国际快递",
            "delivery_time": "3-5个工作日",
            "warranty_info": "个人出售，不提供质保",
            "contact_name": "김철수",
            "contact_email": "kim.cs@example.com",
            "contact_phone": "+82-10-1234-5678",
            "company_name": "서울전자부품",
            "images": json.dumps([
                "https://example.com/images/samsung_ddr5_1.jpg",
                "https://example.com/images/samsung_ddr5_2.jpg"
            ]),
            "expires_at": datetime.now() + timedelta(days=60),
            "tags": json.dumps(["内存", "DDR5", "三星", "服务器", "32GB"]),
            "keywords": "DDR5,内存,Samsung,三星,32GB,服务器",
            "is_verified": True,
            "is_featured": False,
            "is_urgent": False,
            "view_count": 67,
            "inquiry_count": 3,
            "favorite_count": 5,
            "created_by": admin_user.id
        },
        
        # 求购信息 (15条)
        {
            "title": "求购 AMD Ryzen 9 7950X 处理器",
            "description": "公司项目需要，求购AMD Ryzen 9 7950X处理器1-2颗，要求全新或99新，有发票优先。价格合理可长期合作。",
            "listing_type": ListingType.BUY,
            "status": ListingStatus.ACTIVE,
            "product_name": "Ryzen 9 7950X",
            "manufacturer": "AMD",
            "model_number": "7950X",
            "part_number": "100-100000514WOF",
            "category": "处理器",
            "subcategory": "桌面处理器",
            "specifications": json.dumps({
                "核心数": "16核心",
                "线程数": "32线程",
                "基础频率": "4.5 GHz",
                "最大频率": "5.7 GHz",
                "缓存": "80MB",
                "接口": "AM5"
            }),
            "quantity": 2,
            "min_order_quantity": 1,
            "condition": ProductCondition.NEW,
            "condition_notes": "要求全新或99新，有包装盒",
            "price": 600.0,
            "currency": "USD",
            "price_type": PriceType.NEGOTIABLE,
            "total_value": 1200.0,
            "country": "日本",
            "state_province": "东京都",
            "city": "东京",
            "shipping_from": "Tokyo, Japan",
            "payment_terms": "银行转账、信用卡",
            "shipping_terms": "买方承担运费",
            "delivery_time": "尽快",
            "warranty_info": "要求原厂质保",
            "contact_name": "田中太郎",
            "contact_email": "tanaka@example.com",
            "contact_phone": "+81-90-1234-5678",
            "company_name": "東京テクノロジー株式会社",
            "expires_at": datetime.now() + timedelta(days=30),
            "tags": json.dumps(["求购", "AMD", "Ryzen", "7950X", "处理器"]),
            "keywords": "求购,AMD,Ryzen,7950X,处理器,CPU",
            "is_verified": True,
            "is_featured": True,
            "is_urgent": True,
            "view_count": 234,
            "inquiry_count": 15,
            "favorite_count": 8,
            "created_by": admin_user.id
        },
        {
            "title": "长期收购各种型号的SSD固态硬盘",
            "description": "专业回收商，长期大量收购各品牌SSD固态硬盘，包括企业级、消费级产品。价格公道，现金结算，可上门收购。",
            "listing_type": ListingType.BUY,
            "status": ListingStatus.ACTIVE,
            "product_name": "SSD固态硬盘",
            "manufacturer": "各品牌",
            "category": "存储设备",
            "subcategory": "固态硬盘",
            "specifications": json.dumps({
                "类型": "SSD固态硬盘",
                "接口": "SATA/NVMe/PCIe",
                "容量": "256GB及以上",
                "品牌": "三星/英特尔/西数/东芝等"
            }),
            "quantity": 1000,
            "min_order_quantity": 10,
            "condition": ProductCondition.GOOD,
            "condition_notes": "接受各种成色，功能正常即可",
            "price": 50.0,
            "currency": "USD",
            "price_type": PriceType.NEGOTIABLE,
            "country": "中国",
            "state_province": "上海市",
            "city": "上海",
            "shipping_from": "上海市浦东新区",
            "payment_terms": "现金、银行转账",
            "shipping_terms": "可上门收购",
            "delivery_time": "随时",
            "contact_name": "李经理",
            "contact_email": "li.manager@example.com",
            "contact_phone": "+86-139-0000-5678",
            "company_name": "上海电子回收有限公司",
            "expires_at": datetime.now() + timedelta(days=365),
            "tags": json.dumps(["求购", "SSD", "固态硬盘", "回收", "长期"]),
            "keywords": "求购,SSD,固态硬盘,回收,长期收购",
            "is_verified": True,
            "is_featured": True,
            "is_urgent": False,
            "view_count": 445,
            "inquiry_count": 28,
            "favorite_count": 15,
            "created_by": admin_user.id
        }
    ]
    
    # 生成更多随机交易数据
    additional_listings = generate_additional_listings(admin_user.id, len(listings_data))
    listings_data.extend(additional_listings)
    
    print(f"准备创建 {len(listings_data)} 条交易信息...")
    
    # 批量创建交易信息
    for listing_data in listings_data:
        listing = MarketplaceListing(**listing_data)
        db.add(listing)
    
    db.commit()
    print(f"✅ 创建了 {len(listings_data)} 条交易信息")

def generate_additional_listings(admin_user_id: int, existing_count: int):
    """生成额外的交易信息数据"""
    
    additional_listings = []
    
    # 产品模板
    products = [
        {"name": "RTX 3080", "manufacturer": "NVIDIA", "category": "显卡", "price_range": (500, 800)},
        {"name": "RX 6800 XT", "manufacturer": "AMD", "category": "显卡", "price_range": (400, 600)},
        {"name": "i7-12700K", "manufacturer": "Intel", "category": "处理器", "price_range": (300, 400)},
        {"name": "Ryzen 7 5800X", "manufacturer": "AMD", "category": "处理器", "price_range": (250, 350)},
        {"name": "32GB DDR4", "manufacturer": "Corsair", "category": "内存", "price_range": (100, 200)},
        {"name": "1TB NVMe SSD", "manufacturer": "Samsung", "category": "存储", "price_range": (80, 150)},
        {"name": "RTX 3070", "manufacturer": "NVIDIA", "category": "显卡", "price_range": (400, 600)},
        {"name": "i5-12600K", "manufacturer": "Intel", "category": "处理器", "price_range": (200, 300)},
    ]
    
    countries = ["中国", "美国", "日本", "韩国", "德国", "英国", "加拿大", "澳大利亚"]
    conditions = [ProductCondition.NEW, ProductCondition.LIKE_NEW, ProductCondition.EXCELLENT, ProductCondition.GOOD]
    listing_types = [ListingType.SELL, ListingType.BUY]
    
    # 生成剩余交易信息
    for i in range(existing_count, 50):  # 生成50条交易信息
        product = random.choice(products)
        listing_type = random.choice(listing_types)
        condition = random.choice(conditions)
        country = random.choice(countries)
        
        # 根据交易类型生成标题
        if listing_type == ListingType.SELL:
            title_prefix = random.choice(["出售", "转让", "急售", "低价出"])
        else:
            title_prefix = random.choice(["求购", "收购", "寻找", "需要"])
        
        title = f"{title_prefix} {product['name']} {product['manufacturer']}"
        
        # 生成价格
        price_min, price_max = product['price_range']
        if condition == ProductCondition.NEW:
            price = random.uniform(price_max * 0.9, price_max)
        elif condition == ProductCondition.LIKE_NEW:
            price = random.uniform(price_max * 0.8, price_max * 0.9)
        elif condition == ProductCondition.EXCELLENT:
            price = random.uniform(price_max * 0.7, price_max * 0.8)
        else:
            price = random.uniform(price_min, price_max * 0.7)
        
        listing_data = {
            "title": title,
            "description": f"{'出售' if listing_type == ListingType.SELL else '求购'}{product['name']}，{product['manufacturer']}品牌，{'成色' if listing_type == ListingType.SELL else '要求'}{'全新' if condition == ProductCondition.NEW else '良好'}。价格{'可议' if random.choice([True, False]) else '固定'}，{'诚心' if listing_type == ListingType.BUY else '急'}{'求购' if listing_type == ListingType.BUY else '售'}。",
            "listing_type": listing_type,
            "status": ListingStatus.ACTIVE,
            "product_name": product['name'],
            "manufacturer": product['manufacturer'],
            "model_number": f"{product['name']}-{random.randint(1000, 9999)}",
            "category": product['category'],
            "quantity": random.randint(1, 5),
            "condition": condition,
            "condition_notes": f"{'全新未拆封' if condition == ProductCondition.NEW else '使用正常，外观良好'}",
            "price": round(price, 2),
            "currency": "USD",
            "price_type": random.choice([PriceType.FIXED, PriceType.NEGOTIABLE]),
            "total_value": round(price * random.randint(1, 3), 2),
            "country": country,
            "city": f"{country}某市",
            "payment_terms": random.choice(["支付宝、微信", "PayPal", "银行转账", "现金交易"]),
            "shipping_terms": random.choice(["包邮", "买家承担运费", "面交优先"]),
            "delivery_time": random.choice(["1-2天", "3-5天", "1周内", "现货"]),
            "contact_name": f"用户{i+1}",
            "contact_email": f"user{i+1}@example.com",
            "contact_phone": f"+86-138-0000-{1000+i:04d}",
            "expires_at": datetime.now() + timedelta(days=random.randint(7, 90)),
            "tags": json.dumps([product['category'], product['manufacturer'], product['name']]),
            "keywords": f"{product['name']},{product['manufacturer']},{product['category']}",
            "is_verified": random.choice([True, False]),
            "is_featured": random.choice([True, False]) if random.random() < 0.3 else False,
            "is_urgent": random.choice([True, False]) if random.random() < 0.2 else False,
            "view_count": random.randint(10, 500),
            "inquiry_count": random.randint(0, 20),
            "favorite_count": random.randint(0, 15),
            "created_by": admin_user_id
        }
        
        additional_listings.append(listing_data)
    
    return additional_listings

def main():
    """主函数"""
    print("🚀 开始初始化二手交易数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建交易数据
        create_marketplace_data(db)
        
        print("✅ 二手交易数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 二手交易数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
