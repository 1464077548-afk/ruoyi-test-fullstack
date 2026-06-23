"""
性能测试专用 fixtures
"""
import pytest
import time
import statistics
import logging
from typing import Dict, List, Any
from pathlib import Path
import sys
import os
import uuid

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


from common.logger import get_logger
logger = get_logger(__name__)

# =============================================================================
# 性能配置 Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def performance_config() -> Dict[str, Any]:
    """性能测试配置"""
    return {
        'warm_up_requests': 10,
        'test_requests': 100,
        'concurrent_users': [1, 5, 10, 20, 50],
        'ramp_up_time': 30,  # 秒
        'test_duration': 300,  # 秒
        'thresholds': {
            'p50': 200,  # ms
            'p90': 500,
            'p95': 1000,
            'p99': 2000,
            'error_rate': 0.1,  # %
        }
    }


@pytest.fixture(scope="session")
def load_profile() -> Dict[str, Any]:
    """负载配置文件"""
    return {
        'smoke': {
            'users': 10,
            'spawn_rate': 2,
            'duration': 60
        },
        'load': {
            'users': 100,
            'spawn_rate': 10,
            'duration': 300
        },
        'stress': {
            'users': 500,
            'spawn_rate': 50,
            'duration': 600
        },
        'endurance': {
            'users': 50,
            'spawn_rate': 5,
            'duration': 7200  # 2 小时
        }
    }


# =============================================================================
# 性能指标 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def performance_metrics() -> Dict[str, Any]:
    """性能指标收集器"""
    metrics = {
        'response_times': [],
        'success_count': 0,
        'failure_count': 0,
        'start_time': None,
        'end_time': None,
    }
    
    yield metrics
    
    # 计算统计信息
    if metrics['response_times']:
        times = metrics['response_times']
        metrics['avg'] = sum(times) / len(times)
        metrics['min'] = min(times)
        metrics['max'] = max(times)
        metrics['p95'] = sorted(times)[int(len(times) * 0.95)] if len(times) >= 20 else metrics['max']
        metrics['p99'] = sorted(times)[int(len(times) * 0.99)] if len(times) >= 100 else metrics['max']



@pytest.fixture(scope="function")
def response_time_collector(performance_metrics):
    """响应时间收集器"""
    def collect(response_time: float, success: bool = True):
        performance_metrics['response_times'].append(response_time)
        if success:
            performance_metrics['success_count'] += 1
        else:
            performance_metrics['failure_count'] += 1
    return collect


@pytest.fixture(scope="function")
def performance_report(performance_metrics) -> Dict[str, Any]:
    """生成性能报告"""
    yield performance_metrics

    # 计算统计信息
    times = performance_metrics['response_times']
    if times:
        performance_metrics['statistics'] = {
            'count': len(times),
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'p50': sorted(times)[int(len(times) * 0.50)],
            'p90': sorted(times)[int(len(times) * 0.90)],
            'p95': sorted(times)[int(len(times) * 0.95)],
            'p99': sorted(times)[int(len(times) * 0.99)] if len(times) >= 100 else max(times),
        }

        total = performance_metrics['success_count'] + performance_metrics['failure_count']
        performance_metrics['error_rate'] = (
            performance_metrics['failure_count'] / total * 100 if total > 0 else 0
        )

        performance_metrics['throughput'] = (
            len(times) / (performance_metrics['end_time'] - performance_metrics['start_time'])
            if performance_metrics['end_time'] and performance_metrics['start_time']
            else 0
        )





# =============================================================================
# 并发测试 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def concurrent_executor():
    """并发执行器"""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def execute(func, args_list: List[tuple], max_workers: int = 10) -> List[Any]:
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, *args) for args in args_list]
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({'error': str(e)})
        return results

    return execute


@pytest.fixture(scope="function")
def stress_test_config() -> Dict[str, Any]:
    """压力测试配置"""
    return {
        'initial_users': 10,
        'max_users': 500,
        'step_users': 50,
        'step_duration': 60,  # 每级持续时间 (秒)
        'ramp_up_time': 30,   # 每级爬坡时间 (秒)
    }


# =============================================================================
# 性能断言 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def assert_performance(performance_config):
    """性能断言"""
    def _assert(metrics: Dict[str, Any]):
        stats = metrics.get('statistics', {})
        thresholds = performance_config['thresholds']

        errors = []

        if stats.get('p95', 0) > thresholds['p95']:
            errors.append(f"P95 响应时间 {stats['p95']:.2f}ms > {thresholds['p95']}ms")

        if stats.get('p99', 0) > thresholds['p99']:
            errors.append(f"P99 响应时间 {stats['p99']:.2f}ms > {thresholds['p99']}ms")

        if metrics.get('error_rate', 0) > thresholds['error_rate']:
            errors.append(f"错误率 {metrics['error_rate']:.2f}% > {thresholds['error_rate']}%")

        if errors:
            pytest.fail("\n".join(errors))

        return True

    return _assert


# =============================================================================
# Locust Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def locust_config(settings) -> Dict[str, Any]:
    """Locust 配置"""
    return {
        'host': settings.BASE_URL,
        'headless': True,
        'users': 100,
        'spawn_rate': 10,
        'run_time': '300s',
    }


@pytest.fixture(scope="function")
def locust_runner(settings):
    """Locust 运行器"""
    import subprocess

    def run(locustfile: str, **kwargs):
        cmd = [
            'locust',
            '-f', locustfile,
            '--headless',
            f"--users={kwargs.get('users', 100)}",
            f"--spawn-rate={kwargs.get('spawn_rate', 10)}",
            f"--run-time={kwargs.get('run_time', '300s')}",
            f"--host={kwargs.get('host', settings.BASE_URL)}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }

    return run
