"""
数据清洗和验证工具
用于处理从各种数据源采集的原始供应商数据
"""
import re
import json
from typing import Dict, List, Optional, Tuple
import logging
from urllib.parse import urlparse
import phonenumbers
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)

class DataCleaner:
    """数据清洗器"""
    
    def __init__(self):
        # 国家名称标准化映射
        self.country_mapping = {
            'china': '中国',
            'japan': '日本',
            'south korea': '韩国',
            'korea': '韩国',
            'taiwan': '台湾省',
            'singapore': '新加坡',
            'malaysia': '马来西亚',
            'thailand': '泰国',
            'vietnam': '越南',
            'indonesia': '印尼',
            'philippines': '菲律宾',
            'usa': '美国',
            'united states': '美国',
            'germany': '德国',
            'netherlands': '荷兰',
            'uk': '英国',
            'united kingdom': '英国'
        }
        
        # 供应商类型映射
        self.supplier_type_mapping = {
            'manufacturer': 'manufacturer',
            'distributor': 'distributor',
            'trader': 'trader',
            'service provider': 'service_provider',
            '制造商': 'manufacturer',
            '分销商': 'distributor',
            '贸易商': 'trader',
            '服务商': 'service_provider',
            '代理商': 'distributor',
            '经销商': 'distributor'
        }
        
        # 半导体相关关键词
        self.semiconductor_keywords = [
            'semiconductor', 'chip', 'ic', 'wafer', 'pcb', 'led', 'sensor',
            '半导体', '芯片', '集成电路', '晶圆', '传感器', '电子', '电路板'
        ]
    
    def clean_supplier_data(self, raw_data: Dict) -> Tuple[Dict, List[str]]:
        """
        清洗供应商数据
        返回: (清洗后的数据, 警告信息列表)
        """
        cleaned_data = {}
        warnings = []
        
        # 清洗公司名称
        company_name, name_warnings = self._clean_company_name(raw_data.get('company_name', ''))
        cleaned_data['company_name'] = company_name
        warnings.extend(name_warnings)
        
        # 清洗英文公司名称
        company_name_en = self._clean_text(raw_data.get('company_name_en', ''))
        cleaned_data['company_name_en'] = company_name_en
        
        # 清洗联系信息
        contact_person = self._clean_text(raw_data.get('contact_person', ''))
        cleaned_data['contact_person'] = contact_person
        
        # 清洗邮箱
        email, email_warnings = self._clean_email(raw_data.get('email', ''))
        cleaned_data['email'] = email
        warnings.extend(email_warnings)
        
        # 清洗电话
        phone, phone_warnings = self._clean_phone(raw_data.get('phone', ''))
        cleaned_data['phone'] = phone
        warnings.extend(phone_warnings)
        
        # 清洗网站
        website, website_warnings = self._clean_website(raw_data.get('website', ''))
        cleaned_data['website'] = website
        warnings.extend(website_warnings)
        
        # 清洗地址信息
        country, country_warnings = self._clean_country(raw_data.get('country', ''))
        cleaned_data['country'] = country
        warnings.extend(country_warnings)
        
        cleaned_data['province'] = self._clean_text(raw_data.get('province', ''))
        cleaned_data['city'] = self._clean_text(raw_data.get('city', ''))
        cleaned_data['address'] = self._clean_text(raw_data.get('address', ''))
        
        # 清洗供应商类型
        supplier_type, type_warnings = self._clean_supplier_type(raw_data.get('supplier_type', ''))
        cleaned_data['supplier_type'] = supplier_type
        warnings.extend(type_warnings)
        
        # 清洗企业规模
        scale, scale_warnings = self._determine_company_scale(raw_data)
        cleaned_data['scale'] = scale
        warnings.extend(scale_warnings)
        
        # 清洗数值字段
        cleaned_data['established_year'] = self._clean_year(raw_data.get('established_year'))
        cleaned_data['employee_count'] = self._clean_integer(raw_data.get('employee_count'))
        cleaned_data['annual_revenue'] = self._clean_float(raw_data.get('annual_revenue'))
        
        # 清洗产品信息
        main_products, product_warnings = self._clean_products(raw_data.get('main_products', []))
        cleaned_data['main_products'] = main_products
        warnings.extend(product_warnings)
        
        # 验证是否为半导体相关企业
        is_semiconductor, relevance_warnings = self._validate_semiconductor_relevance(cleaned_data)
        warnings.extend(relevance_warnings)
        
        if not is_semiconductor:
            warnings.append("企业可能与半导体行业不相关")
        
        return cleaned_data, warnings
    
    def _clean_company_name(self, name: str) -> Tuple[str, List[str]]:
        """清洗公司名称"""
        warnings = []
        
        if not name or not name.strip():
            warnings.append("公司名称为空")
            return "", warnings
        
        # 去除多余空格和特殊字符
        cleaned_name = re.sub(r'\s+', ' ', name.strip())
        
        # 检查名称长度
        if len(cleaned_name) < 3:
            warnings.append("公司名称过短")
        elif len(cleaned_name) > 200:
            warnings.append("公司名称过长")
            cleaned_name = cleaned_name[:200]
        
        return cleaned_name, warnings
    
    def _clean_email(self, email: str) -> Tuple[str, List[str]]:
        """清洗邮箱地址"""
        warnings = []
        
        if not email or not email.strip():
            return "", warnings
        
        email = email.strip().lower()
        
        try:
            # 验证邮箱格式
            valid = validate_email(email)
            return valid.email, warnings
        except EmailNotValidError as e:
            warnings.append(f"邮箱格式无效: {str(e)}")
            return "", warnings
    
    def _clean_phone(self, phone: str) -> Tuple[str, List[str]]:
        """清洗电话号码"""
        warnings = []
        
        if not phone or not phone.strip():
            return "", warnings
        
        # 去除非数字字符（保留+、-、空格、括号）
        cleaned_phone = re.sub(r'[^\d+\-\s()]', '', phone.strip())
        
        try:
            # 尝试解析电话号码
            parsed = phonenumbers.parse(cleaned_phone, None)
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                return formatted, warnings
            else:
                warnings.append("电话号码格式可能无效")
                return cleaned_phone, warnings
        except:
            warnings.append("无法解析电话号码")
            return cleaned_phone, warnings
    
    def _clean_website(self, website: str) -> Tuple[str, List[str]]:
        """清洗网站地址"""
        warnings = []
        
        if not website or not website.strip():
            return "", warnings
        
        website = website.strip()
        
        # 添加协议前缀
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        try:
            parsed = urlparse(website)
            if not parsed.netloc:
                warnings.append("网站地址格式无效")
                return "", warnings
            
            return website, warnings
        except:
            warnings.append("无法解析网站地址")
            return "", warnings
    
    def _clean_country(self, country: str) -> Tuple[str, List[str]]:
        """清洗国家名称"""
        warnings = []
        
        if not country or not country.strip():
            warnings.append("国家信息缺失")
            return "", warnings
        
        country_lower = country.strip().lower()
        
        # 标准化国家名称
        if country_lower in self.country_mapping:
            return self.country_mapping[country_lower], warnings
        
        # 如果没有找到映射，返回原始值并添加警告
        warnings.append(f"未识别的国家名称: {country}")
        return country.strip(), warnings
    
    def _clean_supplier_type(self, supplier_type: str) -> Tuple[str, List[str]]:
        """清洗供应商类型"""
        warnings = []
        
        if not supplier_type or not supplier_type.strip():
            warnings.append("供应商类型缺失，默认设为制造商")
            return "manufacturer", warnings
        
        type_lower = supplier_type.strip().lower()
        
        if type_lower in self.supplier_type_mapping:
            return self.supplier_type_mapping[type_lower], warnings
        
        warnings.append(f"未识别的供应商类型: {supplier_type}，默认设为制造商")
        return "manufacturer", warnings
    
    def _determine_company_scale(self, raw_data: Dict) -> Tuple[str, List[str]]:
        """确定企业规模"""
        warnings = []
        
        employee_count = self._clean_integer(raw_data.get('employee_count'))
        annual_revenue = self._clean_float(raw_data.get('annual_revenue'))
        
        # 根据员工数量判断
        if employee_count:
            if employee_count >= 1000:
                return "large", warnings
            elif employee_count >= 100:
                return "medium", warnings
            elif employee_count >= 50:
                return "small", warnings
            else:
                return "startup", warnings
        
        # 根据年营收判断（万美元）
        if annual_revenue:
            if annual_revenue >= 10000:  # 1亿美元
                return "large", warnings
            elif annual_revenue >= 1000:  # 1000万美元
                return "medium", warnings
            elif annual_revenue >= 100:   # 100万美元
                return "small", warnings
            else:
                return "startup", warnings
        
        warnings.append("无法确定企业规模，默认设为中型企业")
        return "medium", warnings
    
    def _clean_products(self, products) -> Tuple[str, List[str]]:
        """清洗产品信息"""
        warnings = []
        
        if not products:
            warnings.append("产品信息缺失")
            return "[]", warnings
        
        if isinstance(products, str):
            try:
                # 尝试解析JSON字符串
                products_list = json.loads(products)
            except:
                # 如果不是JSON，按逗号分割
                products_list = [p.strip() for p in products.split(',') if p.strip()]
        elif isinstance(products, list):
            products_list = [str(p).strip() for p in products if str(p).strip()]
        else:
            products_list = [str(products).strip()]
        
        # 去重和清洗
        cleaned_products = []
        for product in products_list:
            if product and len(product) > 1:
                cleaned_products.append(product)
        
        if not cleaned_products:
            warnings.append("没有有效的产品信息")
            return "[]", warnings
        
        return json.dumps(cleaned_products, ensure_ascii=False), warnings
    
    def _validate_semiconductor_relevance(self, data: Dict) -> Tuple[bool, List[str]]:
        """验证是否与半导体行业相关"""
        warnings = []
        
        # 检查字段
        text_to_check = [
            data.get('company_name', ''),
            data.get('company_name_en', ''),
            data.get('main_products', ''),
            data.get('company_description', '')
        ]
        
        combined_text = ' '.join(text_to_check).lower()
        
        # 检查是否包含半导体相关关键词
        for keyword in self.semiconductor_keywords:
            if keyword.lower() in combined_text:
                return True, warnings
        
        warnings.append("未检测到半导体相关关键词")
        return False, warnings
    
    def _clean_text(self, text: str) -> str:
        """通用文本清洗"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())
    
    def _clean_integer(self, value) -> Optional[int]:
        """清洗整数值"""
        if value is None:
            return None
        try:
            return int(float(str(value)))
        except:
            return None
    
    def _clean_float(self, value) -> Optional[float]:
        """清洗浮点数值"""
        if value is None:
            return None
        try:
            return float(str(value))
        except:
            return None
    
    def _clean_year(self, year) -> Optional[int]:
        """清洗年份"""
        if not year:
            return None
        
        try:
            year_int = int(float(str(year)))
            if 1900 <= year_int <= 2024:
                return year_int
            else:
                return None
        except:
            return None

# 使用示例
if __name__ == "__main__":
    cleaner = DataCleaner()
    
    # 测试数据
    raw_data = {
        'company_name': '  深圳市XX半导体有限公司  ',
        'email': 'SALES@XX-SEMI.COM',
        'phone': '86-755-12345678',
        'website': 'www.xx-semi.com',
        'country': 'china',
        'supplier_type': '制造商',
        'employee_count': '500',
        'main_products': ['集成电路', '传感器', 'LED芯片']
    }
    
    cleaned_data, warnings = cleaner.clean_supplier_data(raw_data)
    
    print("清洗后的数据:")
    print(json.dumps(cleaned_data, ensure_ascii=False, indent=2))
    
    print("\n警告信息:")
    for warning in warnings:
        print(f"- {warning}")
