@echo off
REM 主测试调度脚本
REM 阶段1: 使用pytest-xdist并行执行接口和UI测试
REM 阶段2: 禁用pytest-xdist串行执行性能测试
chcp 65001 >nul
cd /d E:\ruoyi-ui\ruoyi_fullstack_test

set OVERALL_EXIT_CODE=0

echo ========================================
echo  开始执行完整测试套件
echo  时间: %date% %time%
echo ========================================

REM ============================================
REM 阶段1: 接口和UI测试 (并行)
REM ============================================
echo.
echo [阶段 1/2] 开始执行接口和UI测试 (并行)
echo.

call run_api_ui_tests.bat
set API_UI_EXIT_CODE=%ERRORLEVEL%

if not "%API_UI_EXIT_CODE%"=="0" (
    echo [警告] 接口和UI测试有失败用例，退出码: %API_UI_EXIT_CODE%
    echo [继续] 继续执行性能测试...
)

REM ============================================
REM 阶段2: 性能测试 (串行)
REM ============================================
echo.
echo [阶段 2/2] 开始执行性能测试 (串行)
echo.

call run_performance_tests.bat
set PERF_EXIT_CODE=%ERRORLEVEL%

if not "%PERF_EXIT_CODE%"=="0" (
    echo [警告] 性能测试有失败用例，退出码: %PERF_EXIT_CODE%
)

REM ============================================
REM 汇总
REM ============================================
echo.
echo ========================================
echo  完整测试套件执行完毕
echo  时间: %date% %time%
echo  接口和UI测试退出码: %API_UI_EXIT_CODE%
echo  性能测试退出码: %PERF_EXIT_CODE%
echo ========================================

REM 任一阶段失败则整体失败
if not "%API_UI_EXIT_CODE%"=="0" set OVERALL_EXIT_CODE=1
if not "%PERF_EXIT_CODE%"=="0" set OVERALL_EXIT_CODE=1

exit /b %OVERALL_EXIT_CODE%
