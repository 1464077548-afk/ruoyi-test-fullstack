import yaml
import os
from typing import Dict, Optional, Any, List, Union
from enum import Enum
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


class LocatorStrategy(Enum):
    """Playwright 定位策略枚举"""
    # 语义化定位器（推荐优先使用）
    ROLE = "get_by_role"
    TEXT = "get_by_text"
    LABEL = "get_by_label"
    PLACEHOLDER = "get_by_placeholder"
    TEST_ID = "get_by_test_id"
    ALT_TEXT = "get_by_alt_text"
    TITLE = "get_by_title"
    
    # 传统定位器
    CSS = "locator"  # CSS 选择器
    XPATH = "locator"  # XPath 选择器
    ID = "get_by_test_id"  # 也可用 test_id
    
    # 组合/相对定位
    FILTER = "filter"
    FRAME = "frame_locator"
    FIRST = "first"
    LAST = "last"
    NTH = "nth"


@dataclass
class LocatorConfig:
    """定位器配置数据类"""
    strategy: str  # 定位策略
    value: Any  # 定位值
    options: Dict[str, Any] = field(default_factory=dict)  # 额外选项（如 exact, name 等）
    chain: List[Dict[str, Any]] = field(default_factory=list)  # 链式调用配置
    description: str = ""  # 定位器描述
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LocatorConfig':
        """从字典创建"""
        return cls(
            strategy=data.get('strategy', 'css'),
            value=data.get('value'),
            options=data.get('options', {}),
            chain=data.get('chain', []),
            description=data.get('description', '')
        )


class LocatorMap:
    """UI 元素定位配置管理 - 支持 Playwright 定位器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化
        
        Args:
            config_path: 配置文件路径，默认为当前目录下的 locator_map.yaml
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            'locator_map.yaml'
        )
        self.locator_map = self._load_locator_map()
    
    def _load_locator_map(self) -> Dict[str, Any]:
        """加载定位器配置"""
        if not os.path.exists(self.config_path):
            logger.warning(f"配置文件不存在：{self.config_path}，将创建空配置")
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            return config.get('locators', {})
        except Exception as e:
            logger.error(f"加载配置文件失败：{e}")
            return {}
    
    def _get_locator(self, locator_key: str) -> Optional[LocatorConfig]:
        """
        获取定位器配置
        
        Args:
            locator_key: 定位器键，格式如 "login.username_input"
            
        Returns:
            LocatorConfig 对象，包含定位策略和参数
        """
        keys = locator_key.split('.')
        current = self.locator_map 
        
        for key in keys:
            if current is None:
                logger.error(f"❌ 定位器路径中断：{locator_key}")
                return None
            if key not in current:
                logger.error(f"❌ 未找到定位器：{locator_key}")
                return None
            current = current[key]
        
        # 处理不同格式的配置
        if isinstance(current, str):
            # 兼容旧格式：自动判断定位类型
            # 例如：
            # login.username_input: ".el-input__inner"
            return self._parse_legacy_locator(current)
        elif isinstance(current, dict):
            # 新格式：完整配置
            return LocatorConfig.from_dict(current)
        
        logger.error(f"❌ 无效的定位器配置格式：{locator_key}")
        return None
    
    def _parse_legacy_locator(self, value: str) -> LocatorConfig:
        """
        解析旧格式定位器字符串（向后兼容）
        
        Args:
            value: 定位器字符串
            
        Returns:
            LocatorConfig 对象
        """
        if value.startswith('//'):
            return LocatorConfig(strategy='xpath', value=value, description='XPath 定位器')
        elif value.startswith('#'):
            return LocatorConfig(strategy='css', value=value, description='CSS ID 选择器')
        elif value.startswith('.'):
            return LocatorConfig(strategy='css', value=value, description='CSS Class 选择器')
        elif value.startswith('text='):
            return LocatorConfig(strategy='text', value=value[5:], description='文本定位器')
        elif value.startswith('role='):
            return LocatorConfig(strategy='role', value=value[5:], description='角色定位器')
        else:
            # 默认使用 CSS 选择器
            return LocatorConfig(strategy='css', value=value, description='CSS 选择器')
    
    def create_locator(self, page, locator_key: str, **kwargs):
        """
        创建 Playwright Locator 对象
        
        Args:
            page: Playwright page 对象
            locator_key: 定位器键，支持以下格式：
                        1. 配置键：如 "login.username_input"
                        2. 直接CSS选择器：如 ".el-dialog", "#app", "[role='button']"
                        3. XPath选择器：如 "//div[@class='el-dialog']"
            kwargs: 用于替换占位符的参数
            
        Returns:
            Playwright Locator 对象
        """
        # 检测是否是直接的选择器（不是配置键）
        if locator_key.startswith('.') or locator_key.startswith('#') or \
           locator_key.startswith('[') or locator_key.startswith('(') or \
           locator_key.startswith('/') or locator_key.startswith('//'):
            # 直接使用CSS或XPath选择器
            config = self._parse_legacy_locator(locator_key)
        else:
            # 使用配置键查找
            config = self._get_locator(locator_key)
            if not config:
                raise ValueError(f"定位器配置不存在：{locator_key}")
        
        try:
            locator = self._build_locator(page, config, **kwargs)
            return locator
        except Exception as e:
            logger.error(f"创建定位器失败：{locator_key}，错误：{e}")
            raise
    
    def _build_locator(self, page, config: LocatorConfig, **kwargs):
        """
        根据配置构建 Playwright Locator
        
        Args:
            page: Playwright page 对象
            config: LocatorConfig 配置对象
            kwargs: 用于替换占位符的参数
            
        Returns:
            Playwright Locator 对象
        """
        locator = None
        
        # 1. 根据策略创建基础定位器
        strategy = config.strategy
        value = config.value
        options = config.options
        
        # 替换 value 中的占位符
        def replace_placeholders(value):
            if isinstance(value, str):
                for key, val in kwargs.items():
                    value = value.replace(f"{{{{{key}}}}}", str(val))
            return value
        
        value = replace_placeholders(value)
        
        # 替换 options 中的占位符
        for key, val in options.items():
            options[key] = replace_placeholders(val)
        
        logger.debug(f"构建定位器：策略={strategy}, 值={value}, 选项={options}")
        
        if strategy == 'role' or strategy == 'get_by_role':
            locator = page.get_by_role(value, **options)
        elif strategy == 'text' or strategy == 'get_by_text':
            locator = page.get_by_text(value, **options)
        elif strategy == 'label' or strategy == 'get_by_label':
            locator = page.get_by_label(value, **options)
        elif strategy == 'placeholder' or strategy == 'get_by_placeholder':
            locator = page.get_by_placeholder(value, **options)
        elif strategy == 'test_id' or strategy == 'get_by_test_id':
            locator = page.get_by_test_id(value, **options)
        elif strategy == 'alt_text' or strategy == 'get_by_alt_text':
            locator = page.get_by_alt_text(value, **options)
        elif strategy == 'title' or strategy == 'get_by_title':
            locator = page.get_by_title(value, **options)
        elif strategy == 'xpath':
            locator = page.locator(f'xpath={value}')
        elif strategy == 'css':
            locator = page.locator(value)
        elif strategy == 'locator':
            # 通用 locator，value 包含完整选择器
            locator = page.locator(value)
        elif strategy == 'frame_locator':
            # Frame 定位器
            locator = page.frame_locator(value)
        else:
            # 默认使用 CSS
            logger.warning(f"未知定位策略：{strategy}，默认使用 CSS")
            locator = page.locator(value)
        
        # 2. 处理链式调用（组合定位）
        if config.chain:
            locator = self._apply_chain(locator, config.chain, **kwargs)
        
        return locator
    
    def _apply_chain(self, locator, chain: List[Any], **kwargs):
        """
        应用链式调用配置（组合定位策略）
        
        支持两种配置格式：
        1. 字典格式：{"method": "filter", "kwargs": {...}}
        2. 字符串格式：直接写方法名，如 "first", "last"
        
        Args:
            locator: 基础 Locator
            chain: 链式调用配置列表
            kwargs: 用于替换占位符的参数
            
        Returns:
            组合后的 Locator
        """
        for step in chain:
            # 如果是字符串，则转换为字典格式
            if isinstance(step, str):
                method = step
                args = []
                step_kwargs = {}
            else:
                method = step.get('method')
                args = step.get('args', [])
                step_kwargs = step.get('kwargs', {})
            
            # 替换参数中的占位符
            def replace_placeholders(value):
                if isinstance(value, str):
                    for key, val in kwargs.items():
                        value = value.replace(f"{{{{{key}}}}}", str(val))
                return value
            
            # 替换 args 中的占位符
            args = [replace_placeholders(arg) for arg in args]
            
            # 替换 kwargs 中的占位符
            for key, value in step_kwargs.items():
                step_kwargs[key] = replace_placeholders(value)
            
            # 特殊处理一些内置方法
            if method == 'first':
                locator = locator.first
            elif method == 'last':
                locator = locator.last
            elif method == 'nth':
                locator = locator.nth(*args)
            elif method == 'and_':
                locator = locator.and_(locator.page.locator(*args, **step_kwargs))
            elif method == 'or_':
                locator = locator.or_(locator.page.locator(*args, **step_kwargs))
            elif method == 'within':
                # 自定义：在指定容器内查找
                container = step.get('container') if isinstance(step, dict) else None
                if container:
                    locator = locator.page.locator(container).locator(locator)
            else:
                # 通用方法调用（支持 get_by_role, get_by_placeholder, filter, locator 等）
                if hasattr(locator, method):
                    attr = getattr(locator, method)
                    if callable(attr):
                        locator = attr(*args, **step_kwargs)
                    else:
                        # 处理属性（如 first/last 已单独处理，此处兜底）
                        locator = attr
                else:
                    logger.warning(f"Locator 没有方法或属性：{method}")
        return locator
    
    def get_locator_info(self, locator_key: str) -> Optional[Dict[str, Any]]:
        """
        获取定位器信息（用于调试/日志）
        
        Args:
            locator_key: 定位器键
            
        Returns:
            定位器信息字典
        """
        config = self._get_locator(locator_key)
        if not config:
            return None
        
        return {
            'key': locator_key,
            'strategy': config.strategy,
            'value': config.value,
            'options': config.options,
            'chain': config.chain,
            'description': config.description
        }
    
    def get_all_locators(self) -> Dict[str, Any]:
        """获取所有定位器配置"""
        return self.locator_map
    
    def update_locator(self, locator_key: str, locator_config: Union[Dict[str, Any], LocatorConfig]):
        """
        更新定位器配置
        
        Args:
            locator_key: 定位器键
            locator_config: 定位器配置（字典或 LocatorConfig 对象）
        """
        keys = locator_key.split('.')
        current = self.locator_map
        
        # 创建嵌套结构
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 设置配置
        if isinstance(locator_config, LocatorConfig):
            current[keys[-1]] = locator_config.to_dict()
        else:
            current[keys[-1]] = locator_config
    
    def add_locator(self, locator_key: str, strategy: str, value: Any, 
                    options: Optional[Dict] = None, 
                    chain: Optional[List] = None,
                    description: str = ""):
        """
        添加新定位器（便捷方法）
        
        Args:
            locator_key: 定位器键
            strategy: 定位策略
            value: 定位值
            options: 额外选项
            chain: 链式调用配置
            description: 描述
        """
        config = LocatorConfig(
            strategy=strategy,
            value=value,
            options=options or {},
            chain=chain or [],
            description=description
        )
        self.update_locator(locator_key, config)
    
    def save_locator_map(self):
        """保存定位器配置到文件"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    {'locators': self.locator_map}, 
                    f, 
                    ensure_ascii=False, 
                    default_flow_style=False,
                    sort_keys=False
                )
            logger.info(f"✅ 定位器配置已保存：{self.config_path}")
        except Exception as e:
            logger.error(f"保存配置文件失败：{e}")
            raise


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化
    locator_map = LocatorMap()
    
    # ============ 示例 1: 语义化定位器 ============
    # 添加角色定位器
    locator_map.add_locator(
        "login.submit_button",
        strategy="get_by_role",
        value="button",
        options={"name": "登 录", "exact": True},
        description="登录页面提交按钮"
    )
    
    # 添加文本定位器
    locator_map.add_locator(
        "login.error_message",
        strategy="get_by_text",
        value="用户名或密码错误",
        options={"exact": False},
        description="登录错误提示"
    )
    
    # 添加 test_id 定位器（推荐用于测试）
    locator_map.add_locator(
        "login.username_input",
        strategy="get_by_test_id",
        value="username-input",
        description="用户名输入框"
    )
    
    # ============ 示例 2: 组合定位策略 ============
    # 使用 filter 进行组合定位
    locator_map.add_locator(
        "product.available_item",
        strategy="css",
        value=".product-item",
        chain=[
            {
                "method": "filter",
                "kwargs": {"has_text": "有货"}
            },
            {
                "method": "first"
            }
        ],
        description="第一个有货的商品"
    )
    
    # 使用 and/or 组合
    locator_map.add_locator(
        "form.validated_input",
        strategy="css",
        value="input",
        chain=[
            {
                "method": "filter",
                "kwargs": {"has": {"method": "locator", "args": [".valid-icon"]}}
            }
        ],
        description="带验证通过图标的输入框"
    )
    
    # ============ 示例 3: Frame 内定位 ============
    locator_map.add_locator(
        "iframe.submit_button",
        strategy="frame_locator",
        value="#payment-frame",
        chain=[
            {
                "method": "locator",
                "args": ["button[type='submit']"]
            }
        ],
        description="支付 iframe 内的提交按钮"
    )
    
    # ============ 示例 4: 兼容旧格式 ============
    locator_map.update_locator("legacy.xpath_element", "//div[@class='container']")
    locator_map.update_locator("legacy.css_element", "#main-content")
    
    # 保存配置
    locator_map.save_locator_map()
    
    # ============ 在测试中使用 ============
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        
        # 使用语义化定位器
        username_input = locator_map.create_locator(page, "login.username_input")
        username_input.fill("testuser")
        
        # 使用组合定位器
        submit_btn = locator_map.create_locator(page, "login.submit_button")
        submit_btn.click()
        
        browser.close()
    """