@echo off
chcp 65001 >nul
echo ========================================
echo   sish内网穿透启动脚本
echo ========================================
echo.
echo 此脚本使用Windows内置SSH客户端连接到公共sish服务器
echo 将本地Jenkins(8090端口)暴露到公网
echo.
echo 按 Ctrl+C 停止
echo.

ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh

echo.
echo 连接已断开
pause