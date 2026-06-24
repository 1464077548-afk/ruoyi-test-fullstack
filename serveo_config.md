# Serveo内网穿透配置完成

## 当前状态

### 内网穿透已成功启动
- **公网地址**: https://64f31f3fcb347d0d-112-21-37-130.serveousercontent.com
- **本地地址**: http://localhost:8090
- **服务**: Serveo (SSH隧道服务)

### Jenkins Pipeline Job
- **Job名称**: ruoyi-fullstack-test-pipeline
- **定时触发**: 每天晚上9点
- **Webhook触发**: 已配置

## 需要配置的GitHub Secrets

访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions

添加以下Secrets：

| Secret名称 | 值 |
|-----------|-----|
| NGROK_URL | https://64f31f3fcb347d0d-112-21-37-130.serveousercontent.com |
| JENKINS_USERNAME | hjp |
| JENKINS_PASSWORD | Hjp3494911 |

## 创建GitHub Actions工作流

访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/new/main/.github/workflows

文件名：`trigger-jenkins.yml`

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

## 启动Serveo命令

```bash
ssh -o StrictHostKeyChecking=no -R 80:localhost:8090 serveo.net
```

## 注意事项

1. 保持终端打开，Serveo连接需要保持运行
2. 每次重启Serveo会生成新地址，需要更新GitHub Secrets
3. 免费版有访问警告页面（可注册账号移除）
4. 确保网络连接稳定

## 更新日期
2026-06-24