#!/bin/bash

echo "========================================="
echo "执行自动化测试"
echo "========================================="

echo "1. 检查测试运行器容器..."
if ! docker ps | grep -q ruoyi-test-runner; then
    echo "错误: 测试运行器容器未运行"
    exit 1
fi

echo "2. 执行冒烟测试..."
docker exec ruoyi-test-runner pytest -m smoke -v --tb=short --html=reports/html/smoke_report.html --self-contained-html
SMOKE_RESULT=$?

if [ $SMOKE_RESULT -ne 0 ]; then
    echo "冒烟测试失败，终止后续测试"
    exit $SMOKE_RESULT
fi

echo "3. 执行API测试..."
docker exec ruoyi-test-runner pytest -m api -v --tb=short --html=reports/html/api_report.html --self-contained-html -n auto

echo "4. 执行UI测试..."
docker exec ruoyi-test-runner pytest -m ui -v --tb=short --html=reports/html/ui_report.html --self-contained-html -n auto

echo "5. 执行集成测试..."
docker exec ruoyi-test-runner pytest -m integration -v --tb=short --html=reports/html/integration_report.html --self-contained-html

echo "6. 执行性能测试..."
docker exec ruoyi-test-runner pytest -m performance -v --tb=short --html=reports/html/performance_report.html --self-contained-html

echo "7. 执行安全测试..."
docker exec ruoyi-test-runner pytest -m security -v --tb=short --html=reports/html/security_report.html --self-contained-html

echo ""
echo "========================================="
echo "测试执行完成！"
echo "========================================="
echo "报告位置: reports/html/"
ls -la reports/html/