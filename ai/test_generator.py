"""
AI测试生成器 (AI Test Generator)
使用AI模型自动生成测试用例

支持Ollama本地部署和云端API：
- Ollama本地部署（推荐）：无需API Key，保护隐私
- 阿里云DashScope：需要DASHSCOPE_API_KEY
- OpenAI：需要OPENAI_API_KEY

使用方式：
    # 方式1: 自动检测可用服务
    generator = AITestGenerator()
    
    # 方式2: 指定使用Ollama
    generator = AITestGenerator(provider="ollama", model="llama3.2")
    
    # 方式3: 使用云端API
    generator = AITestGenerator(provider="dashscope", model="qwen-turbo")
"""
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from .client import AIClient, create_client

class AITestGenerator:
    """AI测试用例生成器"""
    
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        provider: str = "auto"
    ):
        """
        初始化AI测试生成器
        
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
        self.model = model
        self.provider_name = provider
        
        # 创建统一的AI客户端
        self.ai_client = create_client(
            provider=provider,
            model=model,
            api_key=api_key
        )
        
        # 如果没有指定model，使用客户端的默认model
        if not self.model:
            self.model = self.ai_client.model
        
        print(f"[AITestGenerator] 初始化完成")
        print(f"  - Provider: {self.ai_client.provider}")
        print(f"  - Model: {self.model}")
        print(f"  - 可用: {self.ai_client.is_available()}")
    
    def generate_test_cases_from_swagger(self, swagger_path: str, output_dir: str = "tests/api/level1") -> List[str]:
        """
        从Swagger/OpenAPI文档生成测试用例
        
        Args:
            swagger_path: Swagger JSON文件路径
            output_dir: 输出目录
            
        Returns:
            生成的测试用例文件路径列表
        """
        print(f"📖 读取Swagger文档: {swagger_path}")
        
        # 读取Swagger文档
        with open(swagger_path, 'r', encoding='utf-8') as f:
            swagger_doc = json.load(f)
        
        generated_files = []
        
        # 遍历所有接口路径
        for path, path_item in swagger_doc.get('paths', {}).items():
            for method, operation in path_item.items():
                # 生成测试用例
                test_code = self._generate_test_for_endpoint(path, method, operation)
                
                # 生成文件名
                tag = operation.get('tags', ['default'])[0]
                file_name = f"test_{tag.lower()}_{method.lower()}.py"
                file_path = Path(output_dir) / file_name
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(test_code)
                
                generated_files.append(str(file_path))
                print(f"✅ 生成测试用例: {file_path}")
        
        return generated_files
    
    def _generate_test_for_endpoint(self, path: str, method: str, operation: Dict) -> str:
        """
        为单个接口生成测试用例代码
        
        使用AI模型分析接口文档，生成：
        1. 正常场景测试用例
        2. 异常场景测试用例
        3. 边界值测试用例
        """
        # 构造AI提示词
        prompt = self._build_prompt_for_endpoint(path, method, operation)
        
        # 调用AI模型生成测试用例
        # 这里是示例代码，实际需要调用AI API
        test_code = self._call_ai_model(prompt)
        
        return test_code
    
    def _build_prompt_for_endpoint(self, path: str, method: str, operation: Dict) -> str:
        """构造AI提示词"""
        prompt = f"""
        请根据以下接口信息，生成完整的Pytest测试用例代码。

        接口路径: {path}
        请求方法: {method.upper()}
        接口描述: {operation.get('summary', '')}

        请求参数:
        {json.dumps(operation.get('parameters', []), indent=2, ensure_ascii=False)}

        请求体:
        {json.dumps(operation.get('requestBody', {}), indent=2, ensure_ascii=False)}

        请生成以下测试用例：
        1. P0级：正常场景测试（使用有效数据调用接口，验证返回成功）
        2. P1级：异常场景测试（使用无效数据，验证错误处理）
        3. P2级：边界值测试（测试参数的边界情况）
        4. P3级：性能/安全测试（如SQL注入、XSS等）

        代码要求：
        - 使用Pytest框架
        - 使用参数化测试（@pytest.mark.parametrize）
        - 包含详细的断言
        - 包含allure报告装饰器
        - 代码要完整可运行

        请只返回Python代码，不要包含解释。
        """
        return prompt
    
    def _call_ai_model(self, prompt: str, system: str = None) -> str:
        """
        调用AI模型生成代码
        
        Args:
            prompt: 用户提示词
            system: 系统提示词
            
        Returns:
            AI生成的代码
        """
        # 系统提示词
        if not system:
            system = """你是一个专业的测试工程师，擅长编写高质量的Pytest测试用例。
请生成完整、可运行的Python测试代码，只返回代码，不要包含解释。"""
        
        print("[AITestGenerator] 正在调用AI模型生成测试用例...")
        
        try:
            if self.ai_client.is_available():
                response = self.ai_client.generate(
                    prompt=prompt,
                    system=system,
                    temperature=0.3,  # 较低的temperature使输出更确定性
                    max_tokens=4096
                )
                return response
            else:
                print("[AITestGenerator] AI服务不可用，返回示例代码")
                return self._get_fallback_code()
        except Exception as e:
            print(f"[AITestGenerator] AI调用失败: {e}，返回示例代码")
            return self._get_fallback_code()
    
    def _get_fallback_code(self) -> str:
        """获取备用代码（当AI不可用时）"""
        return '''
"""AI生成的测试用例（示例代码）"""
import pytest
from api.clients.user_client import UserClient
from common.utils.data_factory import DataFactory

class TestUserApi:
    """用户API测试（AI生成）"""
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_list(self, user_client):
        """P0-获取用户列表 - AI生成"""
        response = user_client.get_user_list()
        assert response.get("code") == 200
        assert "total" in response
        assert "rows" in response
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,expected_error", [
        ("admin", "wrong_password", "密码错误"),
        ("nonexistent_user", "admin123", "用户不存在"),
    ])
    def test_login_failure(self, auth_client, username, password, expected_error):
        """P1-登录失败 - AI生成"""
        response = auth_client.login(username, password)
        assert response.get("code") == 500
        assert expected_error in response.get("msg", "")
'''
    
    def generate_test_data(self, schema: Dict, scenario: str = "valid") -> List[Dict]:
        """
        根据JSON Schema生成测试数据
        
        Args:
            schema: JSON Schema
            scenario: 场景类型（valid/invalid/boundary）
            
        Returns:
            测试数据列表
        """
        prompt = f"""
        请根据以下JSON Schema，生成测试数据。

        Schema:
        {json.dumps(schema, indent=2, ensure_ascii=False)}

        生成场景: {scenario}

        请生成：
        1. 正常数据：符合Schema约束的有效数据
        2. 异常数据：违反Schema约束的无效数据
        3. 边界数据：接近边界值的数据

        返回格式：JSON数组，每个元素是一个测试数据对象。
        """
        
        # 调用AI模型
        test_data_json = self._call_ai_model(prompt)
        
        # 解析返回的JSON
        try:
            test_data = json.loads(test_data_json)
            return test_data
        except json.JSONDecodeError:
            print(f"⚠️ AI返回的不是有效JSON: {test_data_json}")
            return []
    
    def analyze_test_gap(self, api_doc_path: str, test_files_dir: str) -> Dict:
        """
        分析测试覆盖度缺口
        
        Args:
            api_doc_path: API文档路径
            test_files_dir: 测试文件目录
            
        Returns:
            覆盖度分析报告
        """
        print(f"📊 分析测试覆盖度缺口...")
        
        # 读取API文档
        with open(api_doc_path, 'r', encoding='utf-8') as f:
            api_doc = json.load(f)
        
        # 读取已有测试文件
        test_endpoints = self._extract_test_endpoints(test_files_dir)
        
        # 分析缺口
        gaps = []
        for path, path_item in api_doc.get('paths', {}).items():
            for method in path_item.keys():
                endpoint_key = f"{method.upper()} {path}"
                if endpoint_key not in test_endpoints:
                    gaps.append({
                        'endpoint': endpoint_key,
                        'method': method,
                        'path': path,
                        'reason': '未覆盖'
                    })
        
        return {
            'total_apis': len([(p, m) for p, pi in api_doc.get('paths', {}).items() for m in pi.keys()]),
            'covered_apis': len(test_endpoints),
            'gap_apis': len(gaps),
            'coverage_rate': len(test_endpoints) / len([(p, m) for p, pi in api_doc.get('paths', {}).items() for m in pi.keys()]) * 100,
            'gaps': gaps
        }
    
    def _extract_test_endpoints(self, test_files_dir: str) -> set:
        """从测试文件中提取已测试的endpoint"""
        # 这里实现从测试代码中解析出被测试的API endpoint
        # 简化实现
        return set()


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化AI测试生成器
    generator = AITestGenerator()
    
    # 从Swagger文档生成测试用例
    # generated_files = generator.generate_test_cases_from_swagger(
    #     swagger_path="docs/api/swagger.json",
    #     output_dir="tests/api/level1"
    # )
    
    # 分析测试覆盖度缺口
    # gap_analysis = generator.analyze_test_gap(
    #     api_doc_path="docs/api/swagger.json",
    #     test_files_dir="tests/api"
    # )
    # print(f"测试覆盖度: {gap_analysis['coverage_rate']:.2f}%")
    
    print("AI测试生成器初始化成功")
