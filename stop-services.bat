@echo off
setlocal enabledelayedexpansion

echo =========================================
echo 停止 RuoYi 全栈测试环境
echo =========================================

echo 1. 停止并移除容器...
docker-compose down

echo 2. 清理临时文件...
rmdir /s /q reports 2>nul
mkdir reports 2>nul

echo.
echo =========================================
echo 服务已停止！
echo =========================================
pause