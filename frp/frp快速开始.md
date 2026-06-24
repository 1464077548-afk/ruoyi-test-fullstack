# frp内网穿透 - 快速开始指南

## 已完成的工作

1. ✅ 下载了frp安装包 (frp_0.61.1_windows_amd64.zip)
2. ✅ 创建了frpc.ini配置文件
3. ✅ 解压脚本已准备好

## 需要您手动完成的步骤

### 步骤1：解压frp

请手动解压 `frp.zip` 文件：
- 右键点击 `frp.zip`
- 选择"全部解压缩..."
- 解压到当前目录（E:\ruoyi-ui\ruoyi_fullstack_test）
- 解压后会看到 `frp` 文件夹，里面有 `frpc.exe`

### 步骤2：启动frp

打开PowerShell或CMD，运行以下命令：

```powershell
cd E:\ruoyi-ui\ruoyi_fullstack_test\frp
.\frpc.exe -c ..\frpc.ini
```

如果遇到执行策略错误，运行：
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\frpc.exe -c ..\frpc.ini
```

### 步骤3：获取公网地址

启动成功后，应该会看到类似输出：
```
[INFO] [core] [1m] [1m] [1m] [1m] [36mlogin to server success
[INFO] [36m[36mstart proxy success
```

此时您的Jenkins已经可以通过以下地址访问：
- **http://jenkins.frps.moe** (主地址)
- 或查看日志中的实际地址

### 步骤4：验证访问

打开浏览器，访问 http://jenkins.frps.moe
应该能看到您的Jenkins界面。

### 步骤5：配置GitHub Secrets

1. 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions
2. 点击 "New repository secret"，添加：

| Secret名称 | 值 |
|-----------|-----|
| NGROK_URL | http://jenkins.frps.moe |
| JENKINS_USERNAME | hjp |
| JENKINS_PASSWORD | Hjp3494911 |

### 步骤6：创建GitHub Actions工作流

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

1. 启动frp后，推送代码到main分支
2. 查看GitHub Actions运行状态
3. 检查Jenkins是否收到构建请求

## 故障排查

### frp连接失败
- 检查网络连接
- 尝试其他公共服务器（见下文）

### 备选frp服务器

如果 `jenkins.frps.moe` 不可用，修改 `frpc.ini` 中的 `server_addr`：

**备选1：**
```
server_addr = 158.178.213.110
server_port = 7000
token = frp888
```

**备选2：**
```
server_addr = 47.251.10.87
server_port = 7000
token = freefrp123
```

## 保持frp运行

frp需要在后台持续运行。可以：
1. 保持终端窗口打开
2. 使用Windows任务计划程序
3. 使用NSSM等工具将frp安装为Windows服务

## 下一步

配置完成后，当您推送代码到GitHub仓库的main分支时，GitHub Actions会自动触发Jenkins构建，实现自动化测试流程！