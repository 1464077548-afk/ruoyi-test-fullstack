# GitHub Actions配置说明

## 工作流文件

创建 `.github/workflows/trigger-jenkins.yml` 文件：

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

## 需要配置的Secrets

在GitHub仓库设置 -> Secrets and variables -> Actions中添加以下Secrets：

1. **NGROK_URL**: ngrok公网地址（如 https://abc123.ngrok.io）
2. **JENKINS_USERNAME**: Jenkins用户名（hjp）
3. **JENKINS_PASSWORD**: Jenkins密码（Hjp3494911）

## 使用说明

1. 启动ngrok将本地Jenkins暴露到公网：
   ```bash
   ngrok http 8090
   ```

2. 在GitHub仓库Secrets中配置ngrok地址

3. 当代码推送到main分支时，GitHub Actions会自动触发Jenkins构建