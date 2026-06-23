"""
AI赋能测试框架演示
展示如何使用AI能力改进测试流程

支持Ollama本地部署和云端API：
- Ollama本地部署（推荐）：无需API Key，保护隐私
- 阿里云DashScope：需要DASHSCOPE_API_KEY环境变量
- OpenAI：需要OPENAI_API_KEY环境变量

运行方式:
    # 自动检测可用服务（推荐）
    python -m ai.demo.ai_demo
    
    # 指定使用Ollama
    python -m ai.demo.ai_demo --provider ollama
    
    # 指定使用DashScope
    python -m ai.demo.ai_demo --provider dashscope
"""
import os
import sys
import argparse

# 修复Windows控制台UTF-8编码问题
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import time
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 导入AI模块
from ai.client import AIClient, create_client
from ai.test_generator import AITestGenerator
from ai.element_locator import AIElementLocator, AISelfHealingLocator
from ai.result_analyzer import AIResultAnalyzer, TestResultCollector


class AIDemo:
    """AI赋能演示类"""
    
    def __init__(self, provider: str = "auto", model: str = None):
        """
        初始化演示
        
        Args:
            provider: AI服务提供商
                - "auto": 自动检测
                - "ollama": 本地Ollama部署
                - "dashscope": 阿里云通义千问
                - "openai": OpenAI API
            model: 模型名称
        """
        print(f"\n{'=' * 60}")
        print("🤖 AI赋能测试框架演示")
        print(f"{'=' * 60}\n")
        
        print("初始化AI客户端...")
        self.provider = provider
        self.model = model
        self.project_root = project_root
        self.demo_dir = self.project_root / "ai" / "demo"
        self.demo_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建AI客户端
        try:
            self.ai_client = create_client(
                provider=provider,
                model=model
            )
            print(f"✅ AI客户端初始化成功")
            print(f"   - Provider: {self.ai_client.provider}")
            print(f"   - Model: {self.ai_client.model}")
            print(f"   - 可用: {self.ai_client.is_available()}")
        except Exception as e:
            print(f"⚠️ AI客户端初始化失败: {e}")
            print("将使用模拟模式演示")
            self.ai_client = None
    
    def run_all_demos(self):
        """运行所有演示"""
        demos = [
            ("1. AI客户端演示", self.demo_ai_client),
            ("2. AI测试生成器演示", self.demo_test_generator),
            ("3. AI元素定位器演示", self.demo_element_locator),
            ("4. AI结果分析器演示", self.demo_result_analyzer),
        ]
        
        for name, demo_func in demos:
            print(f"\n{'=' * 60}")
            print(name)
            print(f"{'=' * 60}\n")
            
            try:
                demo_func()
                print(f"\n✅ {name} 完成")
            except Exception as e:
                print(f"\n❌ {name} 失败: {e}")
                import traceback
                traceback.print_exc()
            
            input("\n按 Enter 继续...")
    
    def demo_ai_client(self):
        """演示AI客户端"""
        print("演示：AI客户端功能\n")
        
        if not self.ai_client:
            print("⚠️ AI客户端未初始化，跳过演示")
            return
        
        print("1. 测试文本生成...")
        response = self.ai_client.generate(
            system="你是一个专业的测试工程师",
            prompt="请用一句话解释自动化测试的重要性",
            temperature=0.7
        )
        print(f"   AI响应: {response[:100]}...")
        
        print("\n2. 列出可用模型...")
        models = self.ai_client.list_models()
        if models:
            print(f"   可用模型: {[m.get('name') for m in models]}")
        else:
            print("   无可用模型信息")
        
        print("\n3. 检查服务可用性...")
        print(f"   服务可用: {self.ai_client.is_available()}")
    
    def demo_test_generator(self):
        """演示AI测试生成器"""
        print("演示：AI测试生成器\n")
        
        print("1. 初始化AI测试生成器...")
        try:
            generator = AITestGenerator(
                provider=self.provider,
                model=self.model
            )
            print(f"   ✅ 初始化成功")
            print(f"      Provider: {generator.ai_client.provider}")
            print(f"      Model: {generator.model}")
        except Exception as e:
            print(f"   ❌ 初始化失败: {e}")
            return
        
        print("\n2. 演示生成测试用例提示词...")
        prompt = generator._build_prompt_for_endpoint(
            "/api/user/list",
            "get",
            {"summary": "获取用户列表", "tags": ["User"]}
        )
        print(f"   提示词长度: {len(prompt)} 字符")
        print(f"   提示词预览:\n{prompt[:200]}...")
        
        print("\n3. 演示调用AI模型...")
        if generator.ai_client.is_available():
            response = generator._call_ai_model(
                prompt[:500],  # 使用较短的提示词进行测试
                system="你是一个测试工程师，请简短回复"
            )
            print(f"   AI响应长度: {len(response)} 字符")
            print(f"   响应预览:\n{response[:200]}...")
        else:
            print("   ⚠️ AI服务不可用，使用模拟响应")
            fallback = generator._get_fallback_code()
            print(f"   模拟响应长度: {len(fallback)} 字符")
    
    def demo_element_locator(self):
        """演示AI元素定位器"""
        print("演示：AI元素定位器\n")
        
        print("1. 初始化AI元素定位器...")
        try:
            # 注意：这里不实际启动浏览器，只演示初始化
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                locator = AIElementLocator(
                    page=page,
                    provider=self.provider,
                    model=self.model
                )
                print(f"   ✅ 初始化成功")
                print(f"      Provider: {locator.ai_client.provider}")
                print(f"      Model: {locator.model}")
                
                browser.close()
                
        except Exception as e:
            print(f"   ⚠️ 初始化失败（可能未安装playwright）: {e}")
            print("   跳过浏览器相关演示")
        
        print("\n2. 演示备用元素定位...")
        from ai.element_locator import AIElementLocator as LocatorClass
        fallback_info = LocatorClass._get_fallback_element_info(None, "登录按钮")
        print(f"   备用选择器: {fallback_info.get('selector')}")
        print(f"   备用文本: {fallback_info.get('text')}")
    
    def demo_result_analyzer(self):
        """演示AI结果分析器"""
        print("演示：AI结果分析器\n")
        
        print("1. 初始化AI结果分析器...")
        try:
            analyzer = AIResultAnalyzer(
                provider=self.provider,
                model=self.model
            )
            print(f"   ✅ 初始化成功")
            print(f"      Provider: {analyzer.ai_client.provider}")
            print(f"      Model: {analyzer.model}")
        except Exception as e:
            print(f"   ❌ 初始化失败: {e}")
            return
        
        print("\n2. 演示失败类型分类...")
        test_cases = [
            ("test_element_not_found", "TimeoutError: element '#btn' not found"),
            ("test_assertion_failed", "AssertionError: expected 200 but got 500"),
            ("test_timeout", "Timeout 10000ms exceeded"),
            ("test_auth_error", "401 Unauthorized"),
        ]
        
        for test_name, error in test_cases:
            failure_type = analyzer._classify_failure(error)
            print(f"   测试: {test_name}")
            print(f"   错误: {error[:50]}...")
            print(f"   分类: {failure_type} ({analyzer.FAILURE_TYPES.get(failure_type)})\n")
        
        print("3. 演示AI分析（模拟）...")
        if analyzer.ai_client.is_available():
            result = analyzer.analyze_failure(
                test_name="test_login_failure",
                error_message="Element '#btnLogin' was not visible after 10 seconds",
                page_url="http://localhost:8081/login"
            )
            print(f"   测试名称: {result.get('test_name')}")
            print(f"   失败类型: {result.get('failure_type_cn')}")
            print(f"   AI分析: {result.get('ai_analysis', '')[:100]}...")
        else:
            print("   ⚠️ AI服务不可用，使用模拟分析")
            result = analyzer.analyze_failure(
                test_name="test_login_failure",
                error_message="Element not found"
            )
            print(f"   模拟分析完成")
            print(f"   失败类型: {result.get('failure_type_cn')}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI赋能测试框架演示')
    parser.add_argument(
        '--provider',
        choices=['auto', 'ollama', 'dashscope', 'openai'],
        default='auto',
        help='AI服务提供商'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='模型名称'
    )
    
    args = parser.parse_args()
    
    # 创建演示实例
    demo = AIDemo(provider=args.provider, model=args.model)
    
    # 运行所有演示
    demo.run_all_demos()
    
    print(f"\n{'=' * 60}")
    print("🎉 所有演示完成！")
    print(f"{'=' * 60}\n")
    
    # 显示Ollama使用提示
    if args.provider == 'auto' or args.provider == 'ollama':
        print("💡 使用Ollama的提示：")
        print("   1. 安装Ollama: https://ollama.com")
        print("   2. 拉取模型: ollama pull llama3.2")
        print("   3. 启动Ollama服务: ollama serve")
        print("   4. 运行演示: python -m ai.demo.ai_demo --provider ollama\n")


if __name__ == "__main__":
    main()
