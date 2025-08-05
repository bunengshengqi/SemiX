"""
半导体行业供应商爬虫
注意：使用前请确保遵守目标网站的robots.txt和使用条款
建议优先使用官方API或合作方式获取数据
"""
import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
import time
import random
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

class SemiconductorCrawler:
    """半导体供应商爬虫"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.delay_range = (1, 3)  # 请求间隔（秒）
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def crawl_industry_associations(self) -> List[Dict]:
        """爬取行业协会会员信息"""
        suppliers = []
        
        # 半导体行业协会网站列表
        association_urls = [
            "https://www.semi.org/en/membership/member-directory",  # SEMI协会
            "https://www.jedec.org/membership/member-companies",     # JEDEC协会
            # 注意：这些是示例URL，实际使用时需要检查robots.txt
        ]
        
        for url in association_urls:
            try:
                await self._random_delay()
                suppliers.extend(await self._crawl_semi_members(url))
            except Exception as e:
                logger.error(f"爬取 {url} 失败: {e}")
        
        return suppliers
    
    async def crawl_exhibition_exhibitors(self) -> List[Dict]:
        """爬取展会参展商信息"""
        suppliers = []
        
        # 主要半导体展会网站
        exhibition_urls = [
            "https://www.semiconchina.org/exhibitors",      # SEMICON China
            "https://www.semiconjapan.org/exhibitors",      # SEMICON Japan
            "https://www.semiconkorea.org/exhibitors",      # SEMICON Korea
            # 注意：这些是示例URL，需要根据实际网站结构调整
        ]
        
        for url in exhibition_urls:
            try:
                await self._random_delay()
                suppliers.extend(await self._crawl_exhibition_exhibitors(url))
            except Exception as e:
                logger.error(f"爬取展会 {url} 失败: {e}")
        
        return suppliers
    
    async def crawl_b2b_platforms(self, keywords: List[str]) -> List[Dict]:
        """爬取B2B平台供应商信息"""
        suppliers = []
        
        # 注意：B2B平台爬取需要特别注意合规性
        # 建议使用官方API或者合作方式获取数据
        
        for keyword in keywords:
            try:
                await self._random_delay()
                # 这里应该实现具体的B2B平台爬取逻辑
                # 由于合规性考虑，这里只提供框架
                logger.info(f"搜索关键词: {keyword}")
            except Exception as e:
                logger.error(f"搜索 {keyword} 失败: {e}")
        
        return suppliers
    
    async def _crawl_semi_members(self, url: str) -> List[Dict]:
        """爬取SEMI协会会员信息"""
        suppliers = []
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 这里需要根据实际网站结构解析
                    # 以下是示例解析逻辑
                    member_elements = soup.find_all('div', class_='member-item')
                    
                    for element in member_elements:
                        supplier = await self._parse_member_element(element)
                        if supplier:
                            suppliers.append(supplier)
                            
        except Exception as e:
            logger.error(f"解析SEMI会员页面失败: {e}")
        
        return suppliers
    
    async def _crawl_exhibition_exhibitors(self, url: str) -> List[Dict]:
        """爬取展会参展商信息"""
        suppliers = []
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 解析参展商信息
                    exhibitor_elements = soup.find_all('div', class_='exhibitor-item')
                    
                    for element in exhibitor_elements:
                        supplier = await self._parse_exhibitor_element(element)
                        if supplier:
                            suppliers.append(supplier)
                            
        except Exception as e:
            logger.error(f"解析展会参展商页面失败: {e}")
        
        return suppliers
    
    async def _parse_member_element(self, element) -> Optional[Dict]:
        """解析会员元素"""
        try:
            # 这里需要根据实际HTML结构调整
            company_name = element.find('h3', class_='company-name')
            contact_info = element.find('div', class_='contact-info')
            
            if company_name:
                supplier = {
                    'company_name': company_name.get_text().strip(),
                    'source': 'semi_association',
                    'data_source_url': element.get('data-url', ''),
                    'collected_at': time.time()
                }
                
                # 解析联系信息
                if contact_info:
                    email_elem = contact_info.find('a', href=lambda x: x and 'mailto:' in x)
                    if email_elem:
                        supplier['email'] = email_elem.get('href').replace('mailto:', '')
                    
                    website_elem = contact_info.find('a', class_='website')
                    if website_elem:
                        supplier['website'] = website_elem.get('href')
                
                return supplier
                
        except Exception as e:
            logger.error(f"解析会员元素失败: {e}")
        
        return None
    
    async def _parse_exhibitor_element(self, element) -> Optional[Dict]:
        """解析参展商元素"""
        try:
            # 根据实际HTML结构调整
            company_name = element.find('h4', class_='exhibitor-name')
            booth_info = element.find('span', class_='booth-number')
            
            if company_name:
                supplier = {
                    'company_name': company_name.get_text().strip(),
                    'source': 'exhibition',
                    'booth_number': booth_info.get_text().strip() if booth_info else '',
                    'collected_at': time.time()
                }
                
                return supplier
                
        except Exception as e:
            logger.error(f"解析参展商元素失败: {e}")
        
        return None
    
    async def _random_delay(self):
        """随机延迟，避免过于频繁的请求"""
        delay = random.uniform(*self.delay_range)
        await asyncio.sleep(delay)
    
    def validate_robots_txt(self, url: str) -> bool:
        """检查robots.txt是否允许爬取"""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            # 这里应该实现robots.txt检查逻辑
            # 简化示例，实际应该解析robots.txt内容
            logger.info(f"检查robots.txt: {robots_url}")
            return True
            
        except Exception as e:
            logger.error(f"检查robots.txt失败: {e}")
            return False

# 使用示例
async def run_crawler():
    """运行爬虫示例"""
    async with SemiconductorCrawler() as crawler:
        # 爬取行业协会数据
        association_suppliers = await crawler.crawl_industry_associations()
        print(f"从行业协会采集到 {len(association_suppliers)} 家供应商")
        
        # 爬取展会数据
        exhibition_suppliers = await crawler.crawl_exhibition_exhibitors()
        print(f"从展会采集到 {len(exhibition_suppliers)} 家供应商")
        
        # 合并数据
        all_suppliers = association_suppliers + exhibition_suppliers
        
        # 去重
        unique_suppliers = {}
        for supplier in all_suppliers:
            key = supplier.get('company_name', '').lower()
            if key and key not in unique_suppliers:
                unique_suppliers[key] = supplier
        
        print(f"去重后共 {len(unique_suppliers)} 家供应商")
        
        return list(unique_suppliers.values())

if __name__ == "__main__":
    # 运行爬虫
    suppliers = asyncio.run(run_crawler())
    
    # 保存结果
    with open('crawled_suppliers.json', 'w', encoding='utf-8') as f:
        json.dump(suppliers, f, ensure_ascii=False, indent=2)
