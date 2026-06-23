import os
import json
from config.settings import settings
from datetime import datetime

class Report:
    """报告生成类"""
    
    def __init__(self):
        self.report_dir = settings.REPORT_DIR
        self.html_dir = settings.HTML_DIR
        self.allure_dir = settings.ALLURE_DIR
        
        # 创建报告目录
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.html_dir, exist_ok=True)
        os.makedirs(self.allure_dir, exist_ok=True)
    
    def generate_test_report(self, test_results):
        """生成测试报告"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "results": test_results,
            "summary": self._generate_summary(test_results)
        }
        
        # 生成JSON报告
        report_file = os.path.join(self.report_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return report_file
    
    def _generate_summary(self, test_results):
        """生成报告摘要"""
        total = len(test_results)
        passed = sum(1 for result in test_results if result.get('status') == 'passed')
        failed = sum(1 for result in test_results if result.get('status') == 'failed')
        skipped = sum(1 for result in test_results if result.get('status') == 'skipped')
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": (passed / total * 100) if total > 0 else 0
        }
    
    def generate_performance_report(self, performance_data):
        """生成性能测试报告"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "performance_data": performance_data
        }
        
        # 生成JSON报告
        report_file = os.path.join(self.report_dir, 'performance', f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return report_file
    
    def generate_security_report(self, security_data):
        """生成安全测试报告"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "security_data": security_data
        }
        
        # 生成JSON报告
        report_file = os.path.join(self.report_dir, 'security', f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return report_file

# 全局报告实例
report = Report()

class ComprehensiveReport:
    """综合测试报告"""
    
    def __init__(self):
        self.results = {
            'api': {'total': 0, 'passed': 0, 'failed': 0},
            'ui': {'total': 0, 'passed': 0, 'failed': 0},
            'performance': {'total': 0, 'passed': 0, 'failed': 0},
            'security': {'total': 0, 'passed': 0, 'failed': 0, 'findings': []},
        }
    
    def generate_summary(self) -> dict:
        """生成报告摘要"""
        return {
            'timestamp': datetime.now().isoformat(),
            'overall': {
                'total': sum(r['total'] for r in self.results.values()),
                'passed': sum(r['passed'] for r in self.results.values()),
                'failed': sum(r['failed'] for r in self.results.values()),
                'pass_rate': self.calculate_overall_pass_rate(),
            },
            'by_type': self.results,
            'security_findings': self.results['security']['findings'],
            'performance_metrics': self.get_performance_metrics(),
        }
    
    def calculate_overall_pass_rate(self) -> float:
        """计算整体通过率"""
        total = sum(r['total'] for r in self.results.values())
        passed = sum(r['passed'] for r in self.results.values())
        return (passed / total * 100) if total > 0 else 0