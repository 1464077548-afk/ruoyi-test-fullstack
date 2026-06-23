#!/bin/bash

echo "========================================="
echo "启动 RuoYi 全栈测试环境"
echo "========================================="

echo "1. 检查 Docker 是否运行..."
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker 未运行，请先启动 Docker"
    exit 1
fi

echo "2. 创建必要目录..."
mkdir -p reports/html
mkdir -p reports/junit

echo "3. 构建后端应用..."
cd ../RuoYi-Vue
mvn clean package -DskipTests -q
cd -

echo "4. 构建前端应用..."
cd ../RuoYi-Vue/ruoyi-ui
npm install --production
npm run build:prod
cd -

echo "5. 构建并启动 Docker 服务..."
docker-compose up -d

echo "6. 等待服务启动..."
echo "等待 MySQL 就绪..."
sleep 60

echo "等待 Redis 就绪..."
sleep 30

echo "等待后端服务就绪..."
sleep 120

echo "7. 检查服务健康状态..."
echo "检查 MySQL..."
docker exec ruoyi-mysql mysqladmin ping -h localhost -u root -p123456

echo "检查 Redis..."
docker exec ruoyi-redis redis-cli ping

echo "检查后端服务..."
curl -f http://localhost:8080/api/system/user/getInfo 2>/dev/null || echo "后端服务可能还未完全就绪"

echo ""
echo "========================================="
echo "服务启动完成！"
echo "========================================="
echo "后端服务: http://localhost:8080"
echo "前端服务: http://localhost:80"
echo "测试运行器: ruoyi-test-runner"