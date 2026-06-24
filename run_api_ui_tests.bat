@echo off
chcp 65001 >nul
cd /d E:\ruoyi-ui\ruoyi_fullstack_test

echo ========================================
echo  Phase 1: API and UI Tests (Parallel)
echo ========================================

venv\Scripts\python.exe -m pytest ^
    tests/ ^
    --ignore=tests/performance ^
    -v ^
    --tb=short ^
    --html=reports/html/report_api_ui.html ^
    --self-contained-html ^
    --junitxml=reports/junit/junit_api_ui.xml ^
    --alluredir=reports/allure_api_ui ^
    -n auto ^
    --dist loadscope ^
    --reruns 3 ^
    --reruns-delay 2

set API_UI_EXIT_CODE=%ERRORLEVEL%

echo ========================================
echo  Phase 1 completed, exit code: %API_UI_EXIT_CODE%
echo ========================================

exit /b %API_UI_EXIT_CODE%
