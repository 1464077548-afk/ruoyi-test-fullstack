# sish内网穿透 - 使用Windows内置SSH客户端

## 方案说明

Windows 10/11 自带SSH客户端，不需要下载任何软件！
只需执行一条命令即可将Jenkins暴露到公网。

## 步骤1：检查SSH客户端是否可用

打开PowerShell或CMD，运行：
```powershell
ssh --version
```

如果显示版本信息，则SSH客户端可用。

## 步骤2：启动sish隧道

打开PowerShell或CMD，运行以下命令：

```powershell
ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh
```

## 步骤3：获取公网地址

连接成功后，会显示类似：
```
Forwarding HTTP traffic from https://jenkins.ssi.sh
```

此时您的Jenkins可以通过以下地址访问：
- **https://jenkins.ssi.sh**

## 步骤4：配置GitHub Secrets

1. 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions
2. 添加以下Secrets：

| Secret名称 | 值 |
|-----------|-----|
| NGROK_URL | https://jenkins.ssi.sh |
| JENKINS_USERNAME | hjp |
| JENKINS_PASSWORD | Hjp3494911 |

## 步骤5：创建GitHub Actions工作流

1. 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/new/main/.github/workflows
2. 文件名输入：`trigger-jenkins.yml`
3. 内容：

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

4. 点击 "Commit new file"

## 测试配置

1. 保持SSH连接运行（不要关闭终端）
2. 推送代码到main分支
3. 查看GitHub Actions运行状态
4. 检查Jenkins是否收到构建请求

## 保持连接运行

需要保持终端窗口打开，SSH连接才能持续运行。

如果需要后台运行，可以使用以下方法：

### 方法1：使用Windows Terminal多标签页
- 打开Windows Terminal
- 创建新标签页运行sish命令
- 最小化窗口即可

### 方法2：使用tmux（需要安装）
```powershell
# 安装tmux（需要WSL或git bash）
# 在git bash中运行：
tmux new -s sish
ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh

# 按 Ctrl+B 然后 D 退出到后台
# 恢复会话：tmux attach -t sish
```

### 方法3：使用nohup（需要git bash）
```bash
# 在git bash中运行：
nohup ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh &
```

## 故障排查

### SSH连接失败
- 检查网络连接
- 尝试更换端口：`ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh`
- 尝试其他公共服务器

### 备选公共sish服务器

**服务器1：ssi.sh（推荐）**
```
ssh -p 2222 -R jenkins:80:localhost:8090 ssi.sh
```

**服务器2：备用服务器**
```
ssh -p 2222 -R jenkins:80:localhost:8090 sish.example.com
```

### GitHub Actions无法触发Jenkins
- 确认公网地址可访问
- 检查Jenkins是否正常运行
- 验证Secrets配置是否正确

## 注意事项

- 免费版sish每次重启会更换地址
- 需要保持SSH连接运行
- 如果连接断开，需要重新执行命令

## 下一步

配置完成后，当您推送代码到GitHub仓库的main分支时，GitHub Actions会自动触发Jenkins构建，实现自动化测试流程！