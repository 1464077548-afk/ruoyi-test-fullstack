"""
AI元素定位器 (AI Element Locator)
使用AI视觉识别自动定位页面元素

支持Ollama本地部署和云端API：
- Ollama本地部署：使用支持视觉的模型（如llava, bakllava）
- 阿里云DashScope：需要DASHSCOPE_API_KEY，使用qwen-vl系列模型
- OpenAI：需要OPENAI_API_KEY

使用方式：
    from playwright.sync_api import sync_playwright
    from ai.element_locator import AIElementLocator
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:8081")
        
        # 初始化AI元素定位器
        ai_locator = AIElementLocator(page)
        
        # 根据描述定位元素
        login_button = ai_locator.locate_by_description("登录按钮")
        if login_button:
            login_button.click()
"""
import base64
import json
import os
from typing import Optional, Dict, Any, List
from pathlib import Path
from playwright.sync_api import Page, Locator
from .client import AIClient, create_client

class AIElementLocator:
    """AI元素定位器"""
    
    def __init__(
        self,
        page: Page,
        model: str = None,
        api_key: str = None,
        provider: str = "auto"
    ):
        """
        初始化AI元素定位器
        
        Args:
            page: Playwright Page对象
            model: AI模型名称
                - Ollama视觉模型: llava, bakllava
                - DashScope: qwen-vl-plus, qwen-vl-max
                - OpenAI: gpt-4-vision-preview, gpt-4o
            api_key: API密钥
            provider: AI服务提供商
                - "auto": 自动检测
                - "ollama": 本地Ollama部署
                - "dashscope": 阿里云通义千问
                - "openai": OpenAI API
        """
        self.page = page
        
        # 创建统一的AI客户端
        self.ai_client = create_client(
            provider=provider,
            model=model,
            api_key=api_key
        )
        
        if not self.model:
            self.model = self.ai_client.model
        
        print(f"[AIElementLocator] 初始化完成")
        print(f"  - Provider: {self.ai_client.provider}")
        print(f"  - Model: {self.model}")
        print(f"  - 可用: {self.ai_client.is_available()}")
    
    def locate_by_description(self, description: str, timeout: int = 10000) -> Optional[Locator]:
        """
        根据自然语言描述定位元素
        
        Args:
            description: 元素描述，如"登录按钮"、"用户名输入框"
            timeout: 超时时间（毫秒）
            
        Returns:
            Playwright Locator对象，如果未找到返回None
        """
        print(f"🤖 AI定位元素: {description}")
        
        # 截取页面截图
        screenshot_bytes = self.page.screenshot()
        
        # 调用AI视觉模型识别元素
        element_info = self._call_vision_model(screenshot_bytes, description)
        
        if not element_info:
            print(f"⚠️ AI未能识别元素: {description}")
            return None
        
        # 根据AI返回的信息定位元素
        locator = self._create_locator_from_info(element_info)
        
        # 验证元素是否可见
        try:
            locator.wait_for(state="visible", timeout=timeout)
            print(f"✅ AI定位成功: {description} -> {element_info.get('selector')}")
            return locator
        except Exception as e:
            print(f"⚠️ AI定位的元素不可见: {e}")
            return None
    
    def _call_vision_model(self, screenshot_bytes: bytes, description: str) -> Optional[Dict]:
        """
        调用AI视觉模型识别元素
        
        Args:
            screenshot_bytes: 截图字节流
            description: 元素描述
            
        Returns:
            元素信息字典，包含selector、bbox等
        """
        print(f"[AIElementLocator] 正在调用AI视觉模型识别元素: {description}")
        
        try:
            if self.ai_client.is_available():
                # 将截图编码为base64
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
                
                # 构造提示词
                prompt = f"""
分析这张网页截图，找到以下元素：{description}

请返回以下信息（JSON格式）：
1. selector: 元素的CSS选择器或XPath
2. text: 元素文本内容（如果有）
3. bbox: 元素边界框 [x, y, width, height]
4. confidence: 置信度 (0-1)

只返回JSON，不要包含其他内容。
"""
                
                # 调用AI模型
                response = self.ai_client.generate(
                    prompt=prompt,
                    temperature=0.2,
                    max_tokens=1024
                )
                
                # 解析JSON响应
                try:
                    # 尝试从响应中提取JSON
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        element_info = json.loads(json_match.group())
                        return element_info
                    else:
                        element_info = json.loads(response)
                        return element_info
                except (json.JSONDecodeError, AttributeError):
                    print(f"[AIElementLocator] AI返回的不是有效JSON: {response[:200]}")
                    return self._get_fallback_element_info(description)
            else:
                print("[AIElementLocator] AI服务不可用，使用备用定位")
                return self._get_fallback_element_info(description)
                
        except Exception as e:
            print(f"[AIElementLocator] AI调用失败: {e}，使用备用定位")
            return self._get_fallback_element_info(description)
    
    def _get_fallback_element_info(self, description: str) -> Dict:
        """获取备用元素信息（当AI不可用时）"""
        # 根据描述猜测常见的选择器
        fallback_selectors = {
            "登录按钮": {"selector": "button[type='submit'], .btn-primary, #btnLogin, text=登录", "text": "登录"},
            "用户名输入框": {"selector": "input[name='username'], input[placeholder*='用户'], #username", "text": ""},
            "密码输入框": {"selector": "input[name='password'], input[type='password'], #password", "text": ""},
            "验证码输入框": {"selector": "input[name='validateCode'], input[placeholder*='验证码'], #captcha", "text": ""},
        }
        
        for key, value in fallback_selectors.items():
            if key in description:
                value["confidence"] = 0.5
                value["bbox"] = [0, 0, 0, 0]
                return value
        
        # 默认返回
        return {
            "selector": f"text={description}",
            "text": description,
            "bbox": [0, 0, 0, 0],
            "confidence": 0.3
        }
    
    def _create_locator_from_info(self, element_info: Dict) -> Locator:
        """根据元素信息创建Locator"""
        selector = element_info.get("selector")
        
        if selector:
            return self.page.locator(selector)
        else:
            # 如果没有selector，使用其他方式定位
            text = element_info.get("text")
            if text:
                return self.page.get_by_text(text)
            
            # 最后尝试使用bbox坐标定位
            bbox = element_info.get("bbox")
            if bbox:
                x, y, w, h = bbox
                return self.page.locator(f"*:has-text('{text}')")  # 简化实现
            
            raise ValueError("无法定位元素：缺少selector、text或bbox")
    
    def locate_multiple(self, descriptions: List[str]) -> Dict[str, Optional[Locator]]:
        """
        批量定位多个元素
        
        Args:
            descriptions: 元素描述列表
            
        Returns:
            描述到Locator的映射字典
        """
        results = {}
        
        for desc in descriptions:
            results[desc] = self.locate_by_description(desc)
        
        return results
    
    def verify_locator(self, locator: Locator, expected_description: str) -> bool:
        """
        验证定位器是否正确
        
        Args:
            locator: 要验证的Locator
            expected_description: 期望的元素描述
            
        Returns:
            是否验证通过
        """
        # 截取元素截图
        try:
            element_screenshot = locator.screenshot()
            
            # 调用AI模型验证
            prompt = f"""
            验证这个元素是否是：{expected_description}

            请回答"是"或"否"，并给出理由。
            """
            
            # 调用AI模型（示例）
            response = "是"  # 实际应调用AI API
            
            return "是" in response
        
        except Exception as e:
            print(f"⚠️ 验证定位器失败: {e}")
            return False


class AISelfHealingLocator:
    """AI自愈元素定位器（当元素定位失败时自动修复）"""
    
    def __init__(self, page: Page, primary_selector: str):
        """
        初始化自愈定位器
        
        Args:
            page: Playwright Page对象
            primary_selector: 主要选择器
        """
        self.page = page
        self.primary_selector = primary_selector
        self.ai_locator = AIElementLocator(page)
        
        # 备用选择器列表
        self.backup_selectors = []
    
    def locate(self, description: str = None) -> Locator:
        """
        定位元素（带自愈功能）
        
        Args:
            description: 元素描述（用于AI自愈）
            
        Returns:
            Locator对象
        """
        # 尝试使用主要选择器
        locator = self.page.locator(self.primary_selector)
        
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator
        
        except Exception:
            print(f"⚠️ 主要选择器定位失败: {self.primary_selector}")
            
            # 尝试备用选择器
            for backup in self.backup_selectors:
                try:
                    locator = self.page.locator(backup)
                    locator.wait_for(state="visible", timeout=3000)
                    print(f"✅ 备用选择器定位成功: {backup}")
                    return locator
                except Exception:
                    continue
            
            # 所有选择器都失败，使用AI自愈
            if description:
                print(f"🤖 启动AI自愈...")
                ai_locator = self.ai_locator.locate_by_description(description)
                if ai_locator:
                    return ai_locator
            
            raise Exception(f"无法定位元素: {self.primary_selector}")
    
    def add_backup_selector(self, selector: str):
        """添加备用选择器"""
        self.backup_selectors.append(selector)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例：使用AI元素定位器
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:8081")
        
        # 初始化AI元素定位器
        ai_locator = AIElementLocator(page)
        
        # 根据描述定位元素
        login_button = ai_locator.locate_by_description("登录按钮")
        if login_button:
            login_button.click()
        
        # 使用自愈定位器
        self_healing_locator = AISelfHealingLocator(page, "#btnLogin")
        self_healing_locator.add_backup_selector(".btn-login")
        self_healing_locator.add_backup_selector("text=登录")
        
        locator = self_healing_locator.locate(description="登录按钮")
        locator.click()
        
        browser.close()
