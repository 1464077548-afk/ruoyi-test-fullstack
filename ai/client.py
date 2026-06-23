"""
AI客户端 (AI Client)
统一的AI接口，支持Ollama本地部署和云端API

支持的模式：
1. Ollama本地部署（默认）- 使用OpenAI兼容API
2. 阿里云DashScope（通义千问）- 需要API Key
3. OpenAI - 需要API Key

使用方法：
    # 方式1: 自动检测Ollama
    client = AIClient()
    
    # 方式2: 显式指定Ollama
    client = AIClient(provider="ollama", model="llama3.2")
    
    # 方式3: 使用云端API
    client = AIClient(provider="dashscope", model="qwen-turbo")
    
    # 调用AI生成文本
    response = client.generate("请生成一个测试用例")
"""
import os
import json
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# 尝试导入可选依赖
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import dashscope
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False


class AIClient:
    """
    统一的AI客户端
    
    自动检测可用的AI服务，按优先级使用：
    1. 本地Ollama（推荐，保护隐私，无需API Key）
    2. 阿里云DashScope（需要DASHSCOPE_API_KEY）
    3. OpenAI（需要OPENAI_API_KEY）
    """
    
    # Ollama默认配置
    OLLAMA_DEFAULT_HOST = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL = "llama3.2"
    
    # DashScope默认配置
    DASHSCOPE_DEFAULT_MODEL = "qwen-turbo"
    
    # OpenAI默认配置
    OPENAI_DEFAULT_MODEL = "gpt-4"
    OPENAI_DEFAULT_BASE_URL = "https://api.openai.com/v1"
    
    def __init__(
        self,
        provider: str = "auto",
        model: str = None,
        api_key: str = None,
        base_url: str = None,
        timeout: int = 120,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        初始化AI客户端
        
        Args:
            provider: AI服务提供商
                - "auto": 自动检测可用服务
                - "ollama": 使用本地Ollama
                - "dashscope": 使用阿里云通义千问
                - "openai": 使用OpenAI API
            model: 模型名称
            api_key: API密钥
            base_url: API基础URL（仅Ollama/OpenAI）
            timeout: 请求超时时间（秒）
            temperature: 生成温度
            max_tokens: 最大生成token数
        """
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._provider = None
        self._client = None
        self._api_key = api_key
        
        # 自动检测或使用指定的provider
        if provider == "auto":
            self._auto_detect_provider()
        else:
            self._init_provider(provider, model, api_key, base_url)
    
    def _auto_detect_provider(self):
        """自动检测可用的AI服务"""
        # 优先级：Ollama > DashScope > OpenAI
        if self._check_ollama():
            print("[AI Client] 检测到本地Ollama服务，使用本地部署模式")
            self._init_provider("ollama", self.OLLAMA_DEFAULT_MODEL, None, self.OLLAMA_DEFAULT_HOST)
        elif os.getenv("DASHSCOPE_API_KEY"):
            print("[AI Client] 使用阿里云DashScope（通义千问）")
            self._init_provider("dashscope", self.DASHSCOPE_DEFAULT_MODEL, 
                               os.getenv("DASHSCOPE_API_KEY"), None)
        elif os.getenv("OPENAI_API_KEY"):
            print("[AI Client] 使用OpenAI API")
            self._init_provider("openai", self.OPENAI_DEFAULT_MODEL,
                               os.getenv("OPENAI_API_KEY"), self.OPENAI_DEFAULT_BASE_URL)
        else:
            # 默认使用Ollama，如果不可用则使用模拟模式
            if not self._check_ollama():
                print("[AI Client] 未检测到AI服务，使用模拟模式（返回示例响应）")
                self._provider = "mock"
    
    def _check_ollama(self) -> bool:
        """检查Ollama服务是否可用"""
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{self.OLLAMA_DEFAULT_HOST}/api/tags",
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False
    
    def _init_provider(
        self,
        provider: str,
        model: str,
        api_key: Optional[str],
        base_url: Optional[str]
    ):
        """初始化指定的AI服务"""
        self._provider = provider
        self._model = model
        
        if provider == "ollama":
            self._init_ollama(model, base_url or self.OLLAMA_DEFAULT_HOST)
        elif provider == "dashscope":
            self._init_dashscope(model, api_key)
        elif provider == "openai":
            self._init_openai(model, api_key, base_url or self.OPENAI_DEFAULT_BASE_URL)
        else:
            self._provider = "mock"
    
    def _init_ollama(self, model: str, base_url: str):
        """初始化Ollama客户端"""
        self._model = model or self.OLLAMA_DEFAULT_MODEL
        self._base_url = base_url
        self._provider = "ollama"
        
        if OPENAI_AVAILABLE:
            self._client = openai.OpenAI(
                base_url=f"{base_url}/v1",
                api_key="ollama",  # Ollama不需要真实的API Key
                timeout=self.timeout
            )
        else:
            print("[AI Client] 未安装openai包，Ollama将通过HTTP直接调用")
    
    def _init_dashscope(self, model: str, api_key: Optional[str]):
        """初始化DashScope客户端"""
        if not DASHSCOPE_AVAILABLE:
            print("[AI Client] 未安装dashscope包，将使用HTTP直接调用")
            self._provider = "mock"
            return
            
        self._model = model or self.DASHSCOPE_DEFAULT_MODEL
        self._api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self._provider = "dashscope"
        
        if self._api_key:
            dashscope.api_key = self._api_key
    
    def _init_openai(self, model: str, api_key: Optional[str], base_url: str):
        """初始化OpenAI客户端"""
        if not OPENAI_AVAILABLE:
            print("[AI Client] 未安装openai包，将使用HTTP直接调用")
            self._provider = "mock"
            return
            
        self._model = model or self.OPENAI_DEFAULT_MODEL
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._base_url = base_url
        self._provider = "openai"
        
        if self._api_key:
            self._client = openai.OpenAI(
                api_key=self._api_key,
                base_url=base_url,
                timeout=self.timeout
            )
    
    @property
    def provider(self) -> str:
        """获取当前provider名称"""
        provider_names = {
            "ollama": "Ollama本地部署",
            "dashscope": "阿里云通义千问",
            "openai": "OpenAI",
            "mock": "模拟模式"
        }
        return provider_names.get(self._provider, self._provider)
    
    @property
    def model(self) -> str:
        """获取当前模型名称"""
        return getattr(self, "_model", "unknown")
    
    def generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> str:
        """
        生成文本
        
        Args:
            prompt: 用户提示词
            system: 系统提示词
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        if self._provider == "mock":
            return self._mock_generate(prompt)
        
        if self._provider == "ollama":
            return self._ollama_generate(prompt, system, temperature, max_tokens, **kwargs)
        elif self._provider == "dashscope":
            return self._dashscope_generate(prompt, system, temperature, max_tokens, **kwargs)
        elif self._provider == "openai":
            return self._openai_generate(prompt, system, temperature, max_tokens, **kwargs)
        
        return self._mock_generate(prompt)
    
    def _ollama_generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> str:
        """使用Ollama生成文本"""
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        if OPENAI_AVAILABLE and self._client:
            # 使用OpenAI兼容接口
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        else:
            # 使用HTTP直接调用
            return self._ollama_http_generate(prompt, system, temperature, max_tokens)
    
    def _ollama_http_generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """使用HTTP直接调用Ollama"""
        import urllib.request
        import urllib.error
        
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system:
            payload["system"] = system
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base_url}/api/generate",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer ollama"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "")
        except urllib.error.URLError as e:
            print(f"[AI Client] Ollama调用失败: {e}")
            return self._mock_generate(prompt)
    
    def _dashscope_generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> str:
        """使用DashScope生成文本"""
        if not DASHSCOPE_AVAILABLE:
            return self._mock_generate(prompt)
            
        from dashscope import Generation
        
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = Generation.call(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            result_format="message",
            **kwargs
        )
        
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            print(f"[AI Client] DashScope调用失败: {response.code} - {response.message}")
            return self._mock_generate(prompt)
    
    def _openai_generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> str:
        """使用OpenAI生成文本"""
        if not OPENAI_AVAILABLE or not self._client:
            return self._mock_generate(prompt)
            
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def _mock_generate(self, prompt: str) -> str:
        """模拟生成（当没有可用AI服务时）"""
        print("[AI Client] 警告: 使用模拟模式，返回示例响应")
        return f"[模拟响应] 收到提示词长度: {len(prompt)} 字符\n\n这是模拟的AI响应。在实际使用时，请确保有可用的AI服务。"
    
    def list_models(self) -> List[Dict]:
        """列出可用的模型"""
        if self._provider == "ollama":
            return self._list_ollama_models()
        elif self._provider == "dashscope":
            return [{"name": self._model, "provider": "dashscope"}]
        elif self._provider == "openai":
            return [{"name": self._model, "provider": "openai"}]
        return []
    
    def _list_ollama_models(self) -> List[Dict]:
        """列出Ollama可用模型"""
        import urllib.request
        import urllib.error
        
        try:
            req = urllib.request.Request(
                f"{self._base_url}/api/tags",
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                return [
                    {"name": m.get("name", ""), "provider": "ollama"}
                    for m in result.get("models", [])
                ]
        except urllib.error.URLError:
            return []
    
    def is_available(self) -> bool:
        """检查AI服务是否可用"""
        if self._provider == "mock":
            return False
        if self._provider == "ollama":
            return self._check_ollama()
        return True


# ==================== 便捷函数 ====================

def create_client(
    provider: str = "auto",
    model: str = None,
    api_key: str = None
) -> AIClient:
    """
    创建AI客户端的便捷函数
    
    Args:
        provider: AI服务提供商
        model: 模型名称
        api_key: API密钥
        
    Returns:
        AIClient实例
    """
    return AIClient(provider=provider, model=model, api_key=api_key)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 自动检测
    print("=" * 50)
    print("AI客户端测试")
    print("=" * 50)
    
    # 创建客户端
    client = AIClient()
    
    print(f"当前Provider: {client.provider}")
    print(f"当前模型: {client.model}")
    print(f"服务可用: {client.is_available()}")
    print()
    
    # 测试生成
    print("测试文本生成...")
    response = client.generate(
        system="你是一个专业的测试工程师",
        prompt="请用一句话解释为什么自动化测试很重要"
    )
    print(f"AI响应: {response}")
