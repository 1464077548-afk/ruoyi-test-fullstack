@echo off
chcp 65001 >nul
cd /d E:\ruoyi-ui\ruoyi_fullstack_test

echo ========================================
echo  Phase 2: Performance Tests (Serial)
echo ========================================

venv\Scripts\python.exe -m pytest ^
    tests/performance/ ^
    -v ^
    --tb=short ^
    --html=reports/html/report_performance.html ^
    --self-contained-html ^
    --junitxml=reports/junit/junit_performance.xml ^
    --alluredir=reports/allure_performance ^
    -p no:xdist ^
    -m performance ^
    --reruns 1 ^
    --reruns-delay 5

set PERF_EXIT_CODE=%ERRORLEVEL%

echo ========================================
echo  Phase 2 completed, exit code: %PERF_EXIT_CODE%
echo ========================================

exit /b %PERF_EXIT_CODE%
