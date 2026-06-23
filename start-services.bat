@echo off
setlocal enabledelayedexpansion

echo =========================================
echo 启动 RuoYi 全栈测试环境
echo =========================================

echo 1. 检查 Docker 是否运行...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker 未运行，请先启动 Docker
    pause
    exit /b 1
)

echo 2. 创建必要目录...
mkdir reports\html 2>nul
mkdir reports\junit 2>nul

echo 3. 构建后端应用...
cd ..\RuoYi-Vue
call mvn clean package -DskipTests -q
cd ..\ruoyi_fullstack_test

echo 4. 构建前端应用...
cd ..\RuoYi-Vue\ruoyi-ui
call npm install --production
call npm run build:prod
cd ..\..\ruoyi_fullstack_test

echo 5. 构建并启动 Docker 服务...
docker-compose up -d

echo 6. 等待服务启动...
echo 等待 MySQL 就绪...
timeout /t 60 /nobreak >nul

echo 等待 Redis 就绪...
timeout /t 30 /nobreak >nul

echo 等待后端服务就绪...
timeout /t 120 /nobreak >nul

echo 7. 检查服务健康状态...
echo 检查 MySQL...
docker exec ruoyi-mysql mysqladmin ping -h localhost -u root -p123456

echo 检查 Redis...
docker exec ruoyi-redis redis-cli ping

echo 检查后端服务...
curl -f http://localhost:8080/api/system/user/getInfo 2>nul || echo 后端服务可能还未完全就绪

echo.
echo =========================================
echo 服务启动完成！
echo =========================================
echo 后端服务: http://localhost:8080
echo 前端服务: http://localhost:80
echo 测试运行器: ruoyi-test-runner
pause