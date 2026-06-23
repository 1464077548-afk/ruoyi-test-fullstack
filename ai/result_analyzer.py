"""
AI测试结果分析器 (AI Result Analyzer)
使用AI模型自动分析测试失败原因并提供修复建议

支持Ollama本地部署和云端API：
- Ollama本地部署：无需API Key，保护隐私
- 阿里云DashScope：需要DASHSCOPE_API_KEY
- OpenAI：需要OPENAI_API_KEY

使用方式：
    from ai.result_analyzer import AIResultAnalyzer
    
    # 方式1: 自动检测
    analyzer = AIResultAnalyzer()
    
    # 方式2: 指定Ollama
    analyzer = AIResultAnalyzer(provider="ollama", model="llama3.2")
    
    # 分析失败
    result = analyzer.analyze_failure(
        test_name="test_login",
        error_message="Element not found"
    )
"""
import json
import os
import base64
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
from .client import AIClient, create_client

class AIResultAnalyzer:
    """AI测试结果分析器"""
    
    # 失败类型分类
    FAILURE_TYPES = {
        "ELEMENT_NOT_FOUND": "元素未找到",
        "ASSERTION_FAILED": "断言失败",
        "TIMEOUT": "操作超时",
        "NETWORK_ERROR": "网络错误",
        "AUTH_ERROR": "认证错误",
        "PERMISSION_DENIED": "权限不足",
        "VALIDATION_ERROR": "参数校验失败",
        "UNKNOWN": "未知错误"
    }
    
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        provider: str = "auto"
    ):
        """
        初始化AI结果分析器
        
        Args:
            model: AI模型名称
                - Ollama: llama3.2, qwen2.5, mistral, etc.
                - DashScope: qwen-turbo, qwen-plus, qwen-max
                - OpenAI: gpt-4, gpt-3.5-turbo
            api_key: API密钥（可选）
            provider: AI服务提供商
                - "auto": 自动检测（默认）
                - "ollama": 本地Ollama部署
                - "dashscope": 阿里云通义千问
                - "openai": OpenAI API
        """
        # 创建统一的AI客户端
        self.ai_client = create_client(
            provider=provider,
            model=model,
            api_key=api_key
        )
        
        self.model = self.ai_client.model
        
        print(f"[AIResultAnalyzer] 初始化完成")
        print(f"  - Provider: {self.ai_client.provider}")
        print(f"  - Model: {self.model}")
        print(f"  - 可用: {self.ai_client.is_available()}")
    
    def analyze_failure(
        self,
        test_name: str,
        error_message: str,
        stack_trace: str = None,
        screenshot_path: str = None,
        page_url: str = None,
        logs: str = None
    ) -> Dict:
        """
        分析测试失败原因
        
        Args:
            test_name: 测试名称
            error_message: 错误信息
            stack_trace: 堆栈跟踪
            screenshot_path: 截图路径
            page_url: 页面URL
            logs: 日志内容
            
        Returns:
            分析结果字典
        """
        print(f"🤖 AI分析测试失败: {test_name}")
        
        # 构建分析上下文
        context = {
            "test_name": test_name,
            "error_message": error_message,
            "stack_trace": stack_trace,
            "page_url": page_url,
            "timestamp": datetime.now().isoformat()
        }
        
        # 读取截图
        screenshot_b64 = None
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                screenshot_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 分类失败类型
        failure_type = self._classify_failure(error_message, stack_trace)
        
        # 调用AI模型获取详细分析
        analysis = self._call_ai_analysis(context, screenshot_b64, logs)
        
        # 生成修复建议
        suggestion = self._generate_suggestion(failure_type, analysis, context)
        
        return {
            "test_name": test_name,
            "failure_type": failure_type,
            "failure_type_cn": self.FAILURE_TYPES.get(failure_type, "未知错误"),
            "error_message": error_message,
            "ai_analysis": analysis,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.9  # 置信度
        }
    
    def _classify_failure(self, error_message: str, stack_trace: str = None) -> str:
        """分类失败类型"""
        combined_text = f"{error_message} {stack_trace or ''}".lower()
        
        # 基于关键词分类
        if "timeout" in combined_text or "timed out" in combined_text:
            return "TIMEOUT"
        elif "element" in combined_text and ("not found" in combined_text or "找不到" in combined_text):
            return "ELEMENT_NOT_FOUND"
        elif "assert" in combined_text:
            return "ASSERTION_FAILED"
        elif "401" in combined_text or "unauthorized" in combined_text or "认证失败" in combined_text:
            return "AUTH_ERROR"
        elif "403" in combined_text or "forbidden" in combined_text or "权限" in combined_text:
            return "PERMISSION_DENIED"
        elif "connection" in combined_text or "network" in combined_text or "网络" in combined_text:
            return "NETWORK_ERROR"
        elif "valid" in combined_text or "invalid" in combined_text or "校验" in combined_text:
            return "VALIDATION_ERROR"
        else:
            return "UNKNOWN"
    
    def _call_ai_analysis(self, context: Dict, screenshot_b64: str = None, logs: str = None) -> str:
        """
        调用AI模型进行深度分析
        
        Args:
            context: 分析上下文
            screenshot_b64: 截图base64编码
            logs: 日志内容
            
        Returns:
            AI分析结果
        """
        print(f"[AIResultAnalyzer] 正在调用AI模型分析测试失败...")
        
        try:
            if self.ai_client.is_available():
                # 构造AI提示词
                prompt = f"""
请分析以下测试失败情况，找出根本原因。

测试名称: {context['test_name']}
错误信息: {context['error_message']}
页面URL: {context.get('page_url', 'N/A')}
时间: {context['timestamp']}

堆栈跟踪:
{context.get('stack_trace', 'N/A')}

日志:
{logs or 'N/A'}

请分析：
1. 失败的根本原因是什么？
2. 是前端问题还是后端问题？
3. 应该如何修复这个问题？

请用中文回答，语气专业简洁。
"""
                
                # 调用AI模型
                response = self.ai_client.generate(
                    prompt=prompt,
                    temperature=0.5,
                    max_tokens=2048
                )
                
                return response.strip()
            else:
                print("[AIResultAnalyzer] AI服务不可用，返回示例分析")
                return self._get_fallback_analysis(context)
                
        except Exception as e:
            print(f"[AIResultAnalyzer] AI调用失败: {e}，返回示例分析")
            return self._get_fallback_analysis(context)
    
    def _get_fallback_analysis(self, context: Dict) -> str:
        """获取备用分析（当AI不可用时）"""
        return f"""
失败分析（模拟分析）：

1. 根本原因：
   根据错误信息"{context['error_message']}"，需要详细分析。

2. 问题定位：
   - 请检查错误堆栈
   - 请检查页面状态
   - 请检查测试环境

3. 修复建议：
   - 检查元素选择器
   - 增加等待时间
   - 验证测试数据
"""
    
    def _generate_suggestion(
        self,
        failure_type: str,
        analysis: str,
        context: Dict
    ) -> Dict[str, List[str]]:
        """
        生成修复建议
        
        Args:
            failure_type: 失败类型
            analysis: AI分析结果
            context: 上下文
            
        Returns:
            建议字典
        """
        suggestions = {
            "immediate_actions": [],  # 立即可执行的操作
            "code_changes": [],       # 需要修改代码的操作
            "environment_checks": [],  # 需要检查的环境问题
            "prevention": []           # 预防措施
        }
        
        # 根据失败类型生成针对性建议
        if failure_type == "ELEMENT_NOT_FOUND":
            suggestions["immediate_actions"].append("增加等待时间：使用 wait_for_selector 代替固定等待")
            suggestions["immediate_actions"].append("检查元素选择器是否正确")
            suggestions["code_changes"].append("使用更稳定的选择器（如 data-testid）")
            suggestions["code_changes"].append("考虑使用AI元素定位器自动修复")
            suggestions["prevention"].append("在测试代码中使用语义化的元素定位")
            
        elif failure_type == "TIMEOUT":
            suggestions["immediate_actions"].append("检查网络连接是否稳定")
            suggestions["immediate_actions"].append("增加超时时间配置")
            suggestions["environment_checks"].append("检查被测系统是否响应缓慢")
            suggestions["prevention"].append("对API响应时间设置监控告警")
            
        elif failure_type == "ASSERTION_FAILED":
            suggestions["immediate_actions"].append("检查预期值是否正确")
            suggestions["immediate_actions"].append("验证测试数据是否有效")
            suggestions["code_changes"].append("使用更精确的断言")
            suggestions["prevention"].append("建立测试数据管理机制")
            
        elif failure_type == "AUTH_ERROR":
            suggestions["immediate_actions"].append("检查Token是否过期")
            suggestions["immediate_actions"].append("验证登录状态")
            suggestions["code_changes"].append("实现Token自动刷新机制")
            suggestions["prevention"].append("使用独立的认证Fixture")
            
        elif failure_type == "NETWORK_ERROR":
            suggestions["immediate_actions"].append("检查网络连接")
            suggestions["immediate_actions"].append("重试请求")
            suggestions["environment_checks"].append("检查防火墙/代理设置")
            suggestions["prevention"].append("实现请求重试机制")
        
        return suggestions
    
    def batch_analyze(self, test_results: List[Dict]) -> Dict:
        """
        批量分析测试结果
        
        Args:
            test_results: 测试结果列表
            
        Returns:
            汇总分析报告
        """
        total = len(test_results)
        failed = [r for r in test_results if r.get("status") != "passed"]
        
        # 分类统计
        type_stats = {}
        for result in failed:
            failure_type = result.get("failure_type", "UNKNOWN")
            type_stats[failure_type] = type_stats.get(failure_type, 0) + 1
        
        # 找出重复失败的测试
        duplicate_failures = {}
        for result in failed:
            test_name = result.get("test_name")
            if test_name in duplicate_failures:
                duplicate_failures[test_name] += 1
            else:
                duplicate_failures[test_name] = 1
        
        most_common_failures = sorted(
            duplicate_failures.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 最常失败的测试
        
        return {
            "total_tests": total,
            "passed": total - len(failed),
            "failed": len(failed),
            "pass_rate": (total - len(failed)) / total * 100 if total > 0 else 0,
            "failure_type_stats": {
                self.FAILURE_TYPES.get(k, k): v for k, v in type_stats.items()
            },
            "most_common_failures": [
                {"test_name": name, "count": count}
                for name, count in most_common_failures
            ],
            "detailed_results": failed
        }
    
    def generate_report(self, analysis_result: Dict, output_path: str = None) -> str:
        """
        生成分析报告
        
        Args:
            analysis_result: 分析结果
            output_path: 输出路径
            
        Returns:
            报告内容
        """
        report = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║                  AI 测试结果分析报告                         ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ 测试名称: {analysis_result.get('test_name', 'N/A'):<50} ║
        ║ 失败类型: {analysis_result.get('failure_type_cn', 'N/A'):<50} ║
        ║ 分析时间: {analysis_result.get('timestamp', 'N/A'):<50} ║
        ╚══════════════════════════════════════════════════════════════╝

        【错误信息】
        {analysis_result.get('error_message', 'N/A')}

        【AI分析结果】
        {analysis_result.get('ai_analysis', 'N/A')}

        【修复建议】
        
        立即可执行的操作:
        {self._format_list(analysis_result.get('suggestion', {}).get('immediate_actions', []))}
        
        需要修改代码的操作:
        {self._format_list(analysis_result.get('suggestion', {}).get('code_changes', []))}
        
        需要检查的环境问题:
        {self._format_list(analysis_result.get('suggestion', {}).get('environment_checks', []))}
        
        预防措施:
        {self._format_list(analysis_result.get('suggestion', {}).get('prevention', []))}
        
        【置信度】
        {analysis_result.get('confidence', 0):.0%}
        """
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 分析报告已保存: {output_path}")
        
        return report
    
    def _format_list(self, items: List[str]) -> str:
        """格式化列表"""
        if not items:
            return "  - 无\n"
        return "\n".join([f"  - {item}" for item in items])


class TestResultCollector:
    """测试结果收集器"""
    
    def __init__(self):
        self.results = []
    
    def add_result(
        self,
        test_name: str,
        status: str,
        duration: float,
        error_message: str = None,
        screenshot_path: str = None,
        logs: str = None
    ):
        """添加测试结果"""
        self.results.append({
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "error_message": error_message,
            "screenshot_path": screenshot_path,
            "logs": logs,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_results(self) -> List[Dict]:
        """获取所有结果"""
        return self.results
    
    def get_failed_results(self) -> List[Dict]:
        """获取失败结果"""
        return [r for r in self.results if r.get("status") != "passed"]
    
    def save_to_json(self, output_path: str):
        """保存到JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"✅ 测试结果已保存: {output_path}")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化AI结果分析器
    analyzer = AIResultAnalyzer()
    
    # 分析单个测试失败
    result = analyzer.analyze_failure(
        test_name="test_login_failure",
        error_message="Element '#btnLogin' was not visible after 10 seconds",
        stack_trace="""
        playwright._impl._api_types.TimeoutError: Timeout 10000ms exceeded
        at Locator.waitFor (locator.js:123)
        at LoginPage.click (login_page.py:45)
        """,
        page_url="http://localhost:8081/login"
    )
    
    # 生成报告
    report = analyzer.generate_report(result)
    print(report)
    
    # 批量分析
    collector = TestResultCollector()
    collector.add_result("test_login", "passed", 2.5)
    collector.add_result("test_logout", "failed", 1.0, "元素未找到")
    collector.add_result("test_search", "failed", 3.0, "断言失败")
    
    batch_result = analyzer.batch_analyze(collector.get_results())
    print(f"\n通过率: {batch_result['pass_rate']:.2f}%")
    print(f"失败类型统计: {batch_result['failure_type_stats']}")
