#!/usr/bin/env python3
"""
社区数据初始化脚本 - 创建社区帖子和分类数据
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
from app.models.community import (
    CommunityPost, CommunityCategory, CommunityComment, CommunityLike,
    PostType, PostStatus, PostPriority
)

def create_community_categories(db: Session):
    """创建社区分类"""
    categories_data = [
        {
            "name": "热门话题",
            "name_en": "Hot Topics",
            "description": "当前最热门的半导体行业话题讨论",
            "icon": "fas fa-fire",
            "color": "#ff6b6b",
            "is_featured": True,
            "sort_order": 1
        },
        {
            "name": "问答专区",
            "name_en": "Q&A",
            "description": "专业问题解答，技术难题讨论",
            "icon": "fas fa-question-circle",
            "color": "#4ecdc4",
            "is_featured": True,
            "sort_order": 2
        },
        {
            "name": "经验分享",
            "name_en": "Experience Sharing",
            "description": "成功案例分享，踩坑经验总结",
            "icon": "fas fa-lightbulb",
            "color": "#45b7d1",
            "is_featured": True,
            "sort_order": 3
        },
        {
            "name": "政策解读",
            "name_en": "Policy Analysis",
            "description": "最新政策分析，法规解读",
            "icon": "fas fa-gavel",
            "color": "#f9ca24",
            "is_featured": True,
            "sort_order": 4
        },
        {
            "name": "技术交流",
            "name_en": "Technical Discussion",
            "description": "技术难题讨论，解决方案分享",
            "icon": "fas fa-cogs",
            "color": "#6c5ce7",
            "is_featured": True,
            "sort_order": 5
        },
        {
            "name": "市场分析",
            "name_en": "Market Analysis",
            "description": "市场趋势分析，行业预测",
            "icon": "fas fa-chart-line",
            "color": "#a29bfe",
            "is_featured": True,
            "sort_order": 6
        },
        {
            "name": "供需对接",
            "name_en": "Supply & Demand",
            "description": "商业合作机会，供需信息对接",
            "icon": "fas fa-handshake",
            "color": "#fd79a8",
            "is_featured": True,
            "sort_order": 7
        },
        {
            "name": "新闻资讯",
            "name_en": "News",
            "description": "行业新闻，最新资讯",
            "icon": "fas fa-newspaper",
            "color": "#00b894",
            "is_featured": False,
            "sort_order": 8
        }
    ]
    
    for category_data in categories_data:
        category = CommunityCategory(**category_data)
        db.add(category)
    
    db.commit()
    print(f"✅ 创建了 {len(categories_data)} 个社区分类")

def create_community_posts(db: Session):
    """创建社区帖子数据"""
    
    # 检查是否已有帖子数据
    existing_posts = db.query(CommunityPost).count()
    if existing_posts > 0:
        print(f"已存在 {existing_posts} 条帖子数据")
        return
    
    # 获取admin用户和分类
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        print("❌ 未找到admin用户，请先运行 init_db.py")
        return
    
    categories = db.query(CommunityCategory).all()
    if not categories:
        print("❌ 未找到社区分类，请先创建分类")
        return
    
    # 帖子数据
    posts_data = [
        # 热门话题
        {
            "title": "2024年半导体出海新政策解读：机遇与挑战并存",
            "content": """随着全球半导体产业格局的不断变化，2024年各国政府都出台了新的半导体相关政策。本文将深入分析这些政策对中国半导体企业出海的影响。

## 主要政策变化

### 美国方面
- 《芯片与科学法案》的具体实施细则
- 对华半导体出口管制的最新调整
- 先进制程技术的限制范围扩大

### 欧盟方面
- 《欧洲芯片法案》正式生效
- 对关键原材料的供应链安全要求
- 数字主权战略的推进

### 亚太地区
- 日韩半导体联盟的深化合作
- 东南亚作为替代制造基地的崛起
- 印度半导体制造激励政策

## 对中国企业的影响

**机遇：**
1. 新兴市场需求增长
2. 产业链重构带来的合作机会
3. 技术创新驱动的差异化竞争

**挑战：**
1. 技术出口管制加严
2. 供应链安全审查增多
3. 市场准入门槛提高

## 应对策略建议

1. **多元化市场布局**：不要过度依赖单一市场
2. **技术自主创新**：加大研发投入，提升核心竞争力
3. **合规体系建设**：建立完善的国际合规管理体系
4. **产业链协同**：与上下游企业建立战略合作关系

欢迎大家分享自己的看法和经验！""",
            "summary": "深度解读2024年半导体出海新政策，分析机遇与挑战，提供应对策略建议",
            "post_type": PostType.POLICY,
            "priority": PostPriority.HIGH,
            "category_id": 4,  # 政策解读
            "tags": json.dumps(["政策解读", "出海", "半导体", "2024", "合规"]),
            "keywords": "半导体,出海,政策,芯片法案,合规",
            "is_featured": True,
            "is_official": True,
            "view_count": 1250,
            "like_count": 89,
            "comment_count": 23,
            "created_by": admin_user.id
        },
        
        # 问答专区
        {
            "title": "求助：如何应对美国EAR出口管制清单的最新变化？",
            "content": """我们公司主要生产通信芯片，最近收到客户询问关于EAR（Export Administration Regulations）管制清单的问题。

## 具体情况
- 产品涉及5G通信芯片
- 主要出口市场包括欧洲和东南亚
- 客户担心产品是否受到新的管制影响

## 遇到的问题
1. 如何准确判断产品是否在管制清单内？
2. ECCN分类应该如何确定？
3. 需要申请哪些许可证？
4. 合规流程应该如何建立？

## 已经尝试的方法
- 查阅了BIS官网的相关文件
- 咨询了几家律师事务所
- 参考了同行的做法

但还是有很多不确定的地方，希望有经验的朋友能够指点一下，特别是：

**技术参数判断：**
我们的芯片工作频率在6GHz以下，是否属于管制范围？

**最终用途审查：**
如何证明产品不会用于军事或敏感用途？

**供应链合规：**
上游供应商的合规性如何确保？

非常感谢大家的帮助！🙏""",
            "summary": "通信芯片企业求助EAR出口管制合规问题，涉及ECCN分类、许可证申请等",
            "post_type": PostType.QUESTION,
            "priority": PostPriority.URGENT,
            "category_id": 2,  # 问答专区
            "tags": json.dumps(["求助", "EAR", "出口管制", "通信芯片", "合规"]),
            "keywords": "EAR,出口管制,ECCN,通信芯片,合规",
            "is_urgent": True,
            "view_count": 567,
            "like_count": 34,
            "comment_count": 15,
            "created_by": admin_user.id
        },
        
        # 经验分享
        {
            "title": "成功案例：我们如何在6个月内通过欧盟CE认证",
            "content": """分享一下我们公司最近成功通过欧盟CE认证的经验，希望对准备进入欧洲市场的朋友有所帮助。

## 项目背景
- 产品：工业级传感器芯片
- 目标市场：德国、法国、意大利
- 项目周期：6个月
- 团队规模：5人

## 认证流程

### 第一阶段：准备工作（1个月）
1. **产品技术文档整理**
   - 产品规格书
   - 电路设计图
   - 软件架构文档
   - 风险评估报告

2. **法规研究**
   - EMC指令 2014/30/EU
   - RoHS指令 2011/65/EU
   - 机械指令 2006/42/EC

3. **测试机构选择**
   - 对比了5家认证机构
   - 最终选择TÜV SÜD
   - 费用约15万人民币

### 第二阶段：测试阶段（3个月）
1. **EMC测试**
   - 辐射发射测试
   - 传导发射测试
   - 抗扰度测试
   - 第一次测试失败，主要是辐射超标

2. **整改优化**
   - 增加滤波电路
   - 优化PCB布局
   - 改进屏蔽设计

3. **重新测试**
   - 第二次测试通过
   - 获得测试报告

### 第三阶段：文档准备（1个月）
1. **技术文档**
   - 用户手册（多语言版本）
   - 安装指南
   - 维护手册

2. **符合性声明**
   - DoC文档编写
   - 法律责任声明
   - 授权代表指定

### 第四阶段：最终审核（1个月）
1. **文档审核**
2. **现场审核**
3. **证书颁发**

## 关键经验总结

### 成功要素
1. **提前规划**：在产品设计阶段就考虑认证要求
2. **专业团队**：聘请有经验的认证顾问
3. **充分测试**：预留足够的测试和整改时间
4. **文档管理**：建立完善的文档管理体系

### 常见坑点
1. **技术文档不完整**：很多公司文档准备不充分
2. **测试标准理解错误**：对标准要求理解不准确
3. **时间规划不合理**：低估了整改和重测的时间
4. **成本控制不当**：没有预留足够的认证预算

## 费用明细
- 认证费用：15万人民币
- 整改费用：8万人民币
- 顾问费用：5万人民币
- 总计：28万人民币

## 后续维护
- 每年需要进行监督审核
- 产品变更需要重新评估
- 建立了内部合规管理流程

希望这个经验分享对大家有帮助，有问题欢迎交流！""",
            "summary": "详细分享6个月通过欧盟CE认证的完整流程，包括准备、测试、整改、审核各阶段经验",
            "post_type": PostType.EXPERIENCE,
            "priority": PostPriority.NORMAL,
            "category_id": 3,  # 经验分享
            "tags": json.dumps(["经验分享", "CE认证", "欧盟", "传感器", "合规"]),
            "keywords": "CE认证,欧盟,传感器,合规,经验分享",
            "is_featured": True,
            "is_expert_verified": True,
            "view_count": 892,
            "like_count": 67,
            "comment_count": 28,
            "created_by": admin_user.id
        },
        
        # 技术交流
        {
            "title": "技术讨论：7nm工艺在汽车芯片中的应用前景",
            "content": """最近在研究7nm工艺在汽车电子领域的应用，想和大家讨论一下这个话题。

## 当前现状

### 主流工艺节点
- 汽车芯片主要采用28nm-90nm工艺
- 对先进工艺的需求正在增长
- 成本和可靠性是主要考虑因素

### 7nm工艺优势
1. **性能提升**：更高的运算能力
2. **功耗降低**：对电动汽车续航有利
3. **集成度提高**：减少芯片数量和体积

## 应用场景分析

### 自动驾驶芯片
- 需要强大的AI计算能力
- 7nm工艺可以提供更好的性能功耗比
- 特斯拉、英伟达已有相关产品

### 座舱娱乐系统
- 对图形处理能力要求高
- 需要支持多屏显示
- 7nm工艺有明显优势

### 动力系统控制
- 对实时性要求极高
- 需要考虑温度和振动环境
- 7nm工艺的可靠性需要验证

## 面临的挑战

### 技术挑战
1. **可靠性验证**：汽车级认证周期长
2. **温度范围**：-40°C到+150°C的工作环境
3. **EMC兼容性**：电磁兼容要求严格

### 成本挑战
1. **制造成本**：7nm工艺成本较高
2. **设计成本**：需要重新设计和验证
3. **测试成本**：测试复杂度增加

### 供应链挑战
1. **产能限制**：先进工艺产能有限
2. **供应商集中**：主要依赖台积电、三星
3. **地缘政治**：贸易摩擦影响供应稳定性

## 发展趋势预测

### 短期（1-2年）
- 高端自动驾驶芯片率先采用
- 成本仍然是主要限制因素
- 主要厂商会推出试验性产品

### 中期（3-5年）
- 成本逐步下降，应用范围扩大
- 汽车级认证体系逐步完善
- 中国厂商开始布局相关产品

### 长期（5-10年）
- 7nm成为汽车芯片主流工艺
- 更先进工艺（5nm、3nm）开始应用
- 产业链逐步成熟和本土化

## 讨论问题

1. 大家认为7nm工艺在汽车芯片中的最大应用场景是什么？
2. 如何平衡性能提升和成本增加的矛盾？
3. 中国汽车芯片企业应该如何布局先进工艺？
4. 供应链安全如何保障？

欢迎大家分享观点和经验！""",
            "summary": "深度讨论7nm工艺在汽车芯片中的应用前景，分析技术优势、挑战和发展趋势",
            "post_type": PostType.TECHNICAL,
            "priority": PostPriority.NORMAL,
            "category_id": 5,  # 技术交流
            "tags": json.dumps(["技术讨论", "7nm工艺", "汽车芯片", "自动驾驶", "先进工艺"]),
            "keywords": "7nm,汽车芯片,自动驾驶,先进工艺,技术讨论",
            "is_hot": True,
            "view_count": 734,
            "like_count": 45,
            "comment_count": 31,
            "created_by": admin_user.id
        }
    ]
    
    # 生成更多随机帖子数据
    additional_posts = generate_additional_posts(admin_user.id, categories, len(posts_data))
    posts_data.extend(additional_posts)
    
    print(f"准备创建 {len(posts_data)} 条帖子...")
    
    # 批量创建帖子
    for post_data in posts_data:
        post = CommunityPost(**post_data)
        db.add(post)
    
    db.commit()
    print(f"✅ 创建了 {len(posts_data)} 条帖子")

def generate_additional_posts(admin_user_id: int, categories: list, existing_count: int):
    """生成额外的帖子数据"""
    
    additional_posts = []
    
    # 帖子模板
    post_templates = [
        {
            "title_template": "{}行业最新动态分析",
            "type": PostType.NEWS,
            "priority": PostPriority.NORMAL
        },
        {
            "title_template": "求助：{}相关问题咨询",
            "type": PostType.QUESTION,
            "priority": PostPriority.HIGH
        },
        {
            "title_template": "分享：{}成功经验总结",
            "type": PostType.EXPERIENCE,
            "priority": PostPriority.NORMAL
        },
        {
            "title_template": "讨论：{}技术发展趋势",
            "type": PostType.TECHNICAL,
            "priority": PostPriority.NORMAL
        },
        {
            "title_template": "解读：{}最新政策影响",
            "type": PostType.POLICY,
            "priority": PostPriority.HIGH
        }
    ]
    
    topics = ["芯片设计", "封装测试", "材料工艺", "设备制造", "EDA工具", "IP授权", "供应链管理", "质量控制"]
    
    # 生成剩余帖子
    for i in range(existing_count, 60):  # 生成60条帖子
        template = random.choice(post_templates)
        topic = random.choice(topics)
        category = random.choice(categories)
        
        title = template["title_template"].format(topic)
        
        post_data = {
            "title": title,
            "content": f"这是关于{topic}的详细讨论内容。\n\n## 背景介绍\n\n{topic}是半导体行业的重要组成部分，随着技术的不断发展，相关的挑战和机遇也在不断变化。\n\n## 主要观点\n\n1. 技术发展趋势\n2. 市场机遇分析\n3. 面临的挑战\n4. 应对策略建议\n\n## 结论\n\n希望通过这次讨论，大家能够对{topic}有更深入的了解，欢迎分享你们的观点和经验！",
            "summary": f"关于{topic}的深度分析和讨论，涵盖技术趋势、市场机遇和应对策略",
            "post_type": template["type"],
            "priority": template["priority"],
            "category_id": category.id,
            "tags": json.dumps([topic, "半导体", "讨论", "分析"]),
            "keywords": f"{topic},半导体,技术,讨论",
            "is_featured": random.choice([True, False]) if random.random() < 0.2 else False,
            "is_official": random.choice([True, False]) if random.random() < 0.1 else False,
            "is_expert_verified": random.choice([True, False]) if random.random() < 0.3 else False,
            "is_hot": random.choice([True, False]) if random.random() < 0.15 else False,
            "is_solved": random.choice([True, False]) if template["type"] == PostType.QUESTION and random.random() < 0.6 else False,
            "view_count": random.randint(50, 1000),
            "like_count": random.randint(5, 100),
            "comment_count": random.randint(0, 50),
            "created_by": admin_user_id,
            "created_at": datetime.now() - timedelta(days=random.randint(1, 30)),
            "last_activity_at": datetime.now() - timedelta(hours=random.randint(1, 72))
        }
        
        additional_posts.append(post_data)
    
    return additional_posts

def main():
    """主函数"""
    print("🚀 开始初始化社区数据...")
    
    # 创建数据库表
    create_tables()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建社区分类
        existing_categories = db.query(CommunityCategory).count()
        if existing_categories == 0:
            create_community_categories(db)
        else:
            print(f"已存在 {existing_categories} 个社区分类")
        
        # 创建社区帖子
        create_community_posts(db)
        
        print("✅ 社区数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 社区数据初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
