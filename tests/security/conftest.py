"""
安全测试专用 fixtures
"""
import pytest
from typing import Dict, List, Any
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from common.logger import get_logger
from common.utils.data_factory import DataFactory
from api.clients.auth_client import AuthClient
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from api.clients.base_client import BaseClient

logger = get_logger(__name__)

# =============================================================================
# 安全扫描器 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def owasp_scanner():
    """OWASP 扫描器"""
    from security.scanners.owasp_scanner import OwaspScanner
    settings = Settings()
    scanner = OwaspScanner(base_url=settings.BASE_URL)
    yield scanner
    # OwaspScanner 没有 close 方法，跳过清理


@pytest.fixture(scope="function")
def sql_injection_scanner(authenticated_client):
    """SQL 注入扫描器"""
    from security.scanners.sql_injection import SQLInjectionScanner
    scanner = SQLInjectionScanner(
        base_url=Config.API_BASE_URL,
        token=authenticated_client.token
    )
    yield scanner
    scanner.close()


@pytest.fixture(scope="function")
def xss_scanner(authenticated_client):
    """XSS 扫描器"""
    from security.scanners.xss_scanner import XSSScanner
    scanner = XSSScanner(
        base_url=Config.API_BASE_URL,
        token=authenticated_client.token
    )
    yield scanner
    scanner.close()


@pytest.fixture(scope="function")
def auth_security_scanner():
    """认证安全扫描器"""
    from security.scanners.auth_scanner import AuthSecurityScanner
    settings = Settings()
    scanner = AuthSecurityScanner(base_url=settings.BASE_URL)
    yield scanner
    scanner.close()


@pytest.fixture(scope="function")
def api_security_scanner(authenticated_client):
    """API 安全扫描器"""
    from security.scanners.api_security import APISecurityScanner
    scanner = APISecurityScanner(
        base_url=Config.API_BASE_URL,
        token=authenticated_client.token
    )
    yield scanner
    scanner.close()


# =============================================================================
# 安全测试数据 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def xss_payloads() -> List[str]:
    """XSS 测试载荷"""
    return [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert("XSS")>',
        '<svg onload=alert("XSS")>',
        'javascript:alert("XSS")',
        '<iframe src="javascript:alert(\'XSS\')">',
        "'\"><script>alert('XSS')</script>",
        '<body onload=alert("XSS")>',
        '<input onfocus=alert("XSS") autofocus>',
    ]


@pytest.fixture(scope="function")
def sql_injection_payloads() -> List[str]:
    """SQL 注入测试载荷"""
    return [
        "' OR '1'='1",
        "' OR 1=1 --",
        "'; DROP TABLE users; --",
        "1; SELECT * FROM information_schema.tables",
        "' UNION SELECT NULL, NULL, NULL --",
        "admin'--",
        "1' AND '1'='1",
        "1' AND '1'='2",
        "' OR ''='",
        "1; WAITFOR DELAY '0:0:5' --",
    ]


@pytest.fixture(scope="function")
def path_traversal_payloads() -> List[str]:
    """路径遍历测试载荷"""
    return [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\config\\sam',
        '....//....//etc/passwd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '..%252f..%252f..%252fetc%252fpasswd',
        '/etc/passwd%00.jpg',
    ]


@pytest.fixture(scope="function")
def command_injection_payloads() -> List[str]:
    """命令注入测试载荷"""
    return [
        '; ls -la',
        '| cat /etc/passwd',
        '$(whoami)',
        '`whoami`',
        '; id',
        '|| id',
        '%0Aid',
        '%0Did',
    ]


@pytest.fixture(scope="function")
def weak_passwords() -> List[str]:
    """弱密码列表"""
    return [
        '123456',
        'admin',
        'password',
        'admin123',
        '12345678',
        'qwerty',
        'abc123',
        '111111',
        '123123',
        'iloveyou',
    ]


# =============================================================================
# 安全测试场景 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def security_test_context() -> Dict[str, Any]:
    """安全测试上下文"""
    return {
        'findings': [],
        'vulnerabilities': [],
        'warnings': [],
        'info': [],
    }


@pytest.fixture(scope="function")
def security_report(security_test_context):
    """生成安全报告"""
    yield security_test_context
    
    # 生成报告摘要
    security_test_context['summary'] = {
        'critical': len([v for v in security_test_context['vulnerabilities'] if v.get('severity') == 'CRITICAL']),
        'high': len([v for v in security_test_context['vulnerabilities'] if v.get('severity') == 'HIGH']),
        'medium': len([v for v in security_test_context['vulnerabilities'] if v.get('severity') == 'MEDIUM']),
        'low': len([v for v in security_test_context['vulnerabilities'] if v.get('severity') == 'LOW']),
        'total_findings': len(security_test_context['findings']),
    }


# =============================================================================
# 安全断言 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def assert_no_vulnerability(security_test_context):
    """断言无漏洞"""
    def _assert(vulnerability_type: str = None):
        if vulnerability_type:
            vulns = [v for v in security_test_context['vulnerabilities'] 
                    if v.get('type') == vulnerability_type]
            assert len(vulns) == 0, f"发现 {vulnerability_type} 漏洞：{vulns}"
        else:
            assert len(security_test_context['vulnerabilities']) == 0, \
                f"发现漏洞：{security_test_context['vulnerabilities']}"
        return True
    return _assert


@pytest.fixture(scope="function")
def assert_security_headers():
    """断言安全响应头"""
    def _assert(response, required_headers: List[str] = None):
        if required_headers is None:
            required_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security',
            ]
        
        missing = []
        for header in required_headers:
            if header not in response.headers:
                missing.append(header)
        
        if missing:
            pytest.fail(f"缺少安全响应头：{missing}")
        
        return True
    
    return _assert


# =============================================================================
# 认证安全 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def session_config() -> Dict[str, Any]:
    """会话配置"""
    return {
        'timeout': 1800,  # 30 分钟
        'max_concurrent': 5,
        'secure_cookie': True,
        'http_only': True,
        'same_site': 'Strict',
    }


@pytest.fixture(scope="function")
def token_config() -> Dict[str, Any]:
    """Token 配置"""
    return {
        'algorithm': 'HS256',
        'expiration': 7200,  # 2 小时
        'refresh_expiration': 604800,  # 7 天
    }