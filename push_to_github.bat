@echo off
echo ==============================================
echo 推送项目到 GitHub
echo ==============================================
echo.

set "REPO_URL=https://github.com/1464077548-afk/ruoyi_fullstack_test.git"

echo 步骤 1: 检查 Git 配置...
git config --global user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo 请设置 Git 用户名:
    set /p GIT_USER=用户名：
    git config --global user.name "%GIT_USER%"
)

git config --global user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo 请设置 Git 邮箱:
    set /p GIT_EMAIL=邮箱：
    git config --global user.email "%GIT_EMAIL%"
)

echo.
echo 步骤 2: 添加远程仓库...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo 步骤 3: 推送到 GitHub...
echo 请使用 GitHub 个人访问令牌（Personal Access Token）进行身份验证
echo.
echo 如果您还没有创建 Personal Access Token，请：
echo 1. 访问 https://github.com/settings/tokens
echo 2. 点击 "Generate new token (classic)"
echo 3. 选择 "repo" 权限
echo 4. 生成令牌并复制
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ==============================================
    echo ✅ 推送成功！
    echo ==============================================
    echo 仓库地址: %REPO_URL%
    echo.
) else (
    echo.
    echo ==============================================
    echo ❌ 推送失败，请检查网络和凭证
    echo ==============================================
    echo.
    echo 可能的解决方案:
    echo 1. 确保已安装 Git Credential Manager
    echo 2. 使用 Personal Access Token 代替密码
    echo 3. 检查网络连接
    echo.
)

pause