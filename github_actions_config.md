# GitHub Actions配置说明

## 工作流文件

### 方法一：手动创建工作流文件

在GitHub仓库中创建 `.github/workflows/trigger-jenkins.yml` 文件：

```yaml
name: Trigger Jenkins Build

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  trigger-jenkins:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Jenkins Pipeline
        run: |
          CRUMB=$(curl -s -u "${{ secrets.JENKINS_USERNAME }}:${{ secrets.JENKINS_PASSWORD }}" "${{ secrets.NGROK_URL }}/crumbIssuer/api/json" | jq -r '.crumb')
          curl -X POST "${{ secrets.NGROK_URL }}/job/ruoyi-fullstack-test-pipeline/build" \
            -u "${{ secrets.JENKINS_USERNAME }}:${{ secrets.JENKINS_PASSWORD }}" \
            -H "Jenkins-Crumb: $CRUMB"
```

### 方法二：使用GitHub UI创建

1. 访问仓库页面：https://github.com/1464077548-afk/ruoyi-test-fullstack
2. 点击 "Actions" 选项卡
3. 点击 "New workflow"
4. 搜索 "Simple workflow" 或 "Set up a workflow yourself"
5. 将上述内容粘贴到编辑器中
6. 点击 "Start commit" -> "Commit new file"

## 需要配置的Secrets

在GitHub仓库设置 -> Secrets and variables -> Actions中添加以下Secrets：

1. **NGROK_URL**: ngrok公网地址（如 https://abc123.ngrok.io）
2. **JENKINS_USERNAME**: Jenkins用户名（hjp）
3. **JENKINS_PASSWORD**: Jenkins密码（Hjp3494911）

配置步骤：
1. 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加上述三个Secrets

## 使用说明

### 方式一：使用ngrok（推荐）

1. 启动ngrok将本地Jenkins暴露到公网：
   ```bash
   ngrok http 8090
   ```

2. 在GitHub仓库Secrets中配置ngrok地址（如 https://abc123.ngrok.io）

3. 当代码推送到main分支时，GitHub Actions会自动触发Jenkins构建

### 方式二：使用ngrok配置GitHub Webhook

1. 启动ngrok：
   ```bash
   ngrok http 8090
   ```

2. 在GitHub仓库设置 -> Webhooks中添加：
   - Payload URL: `https://abc123.ngrok.io/generic-webhook-trigger/invoke`
   - Content type: `application/json`
   - Events: Just the push event

## ngrok安装和使用

### Windows安装
```powershell
# 下载ngrok
Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok.zip"

# 解压
Expand-Archive -Path ngrok.zip -DestinationPath . -Force

# 启动
.
grok.exe http 8090
```

### 注册ngrok账号（可选）

访问 https://ngrok.com 注册账号，获取auth token：
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

## 验证配置

1. 启动ngrok后，访问其Web界面查看状态：http://localhost:4040
2. 手动触发GitHub Actions工作流测试
3. 检查Jenkins是否收到构建请求

## 故障排查

### GitHub Actions工作流失败
- 检查Secrets是否正确配置
- 检查ngrok是否正在运行
- 检查Jenkins是否可以正常访问

### Webhook不触发
- 确认ngrok地址正确且正在运行
- 检查GitHub Webhook配置中的Payload URL
- 查看GitHub Webhook的Recent deliveries

### Jenkins构建失败
- 检查Jenkins控制台输出
- 确认Git仓库可访问
- 确认Docker服务正常运行