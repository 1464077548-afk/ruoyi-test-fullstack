# frp内网穿透配置说明（替代ngrok）

## 为什么使用frp？

- ✅ **无需注册**：不需要在第三方网站注册账号
- ✅ **开源免费**：完全开源，社区活跃
- ✅ **可自托管**：可以自己部署frp服务器，也可以使用公共服务器
- ✅ **稳定可靠**：支持TCP、UDP、HTTP、HTTPS等多种协议

## 方案一：使用公共frp服务器（推荐，快速简单）

### 1. 下载frp客户端

访问 https://github.com/fatedier/frp/releases 下载Windows版本：
- 文件名：`frp_0.61.1_windows_amd64.zip`

### 2. 解压并配置

解压到 `E:\ruoyi-ui\ruoyi_fullstack_test\frp` 目录

### 3. 创建frpc.ini配置文件

在 `frp` 目录下创建 `frpc.ini` 文件：

```ini
[common]
server_addr = 47.236.20.222
server_port = 7000
token = frp666

[jenkins]
type = http
local_ip = 127.0.0.1
local_port = 8090
custom_domains = jenkins.frps.moe
```

### 4. 启动frp客户端

```bash
cd E:\ruoyi-ui\ruoyi_fullstack_test\frp
.\frpc.exe -c frpc.ini
```

### 5. 获取公网地址

启动成功后会显示类似：
```
login to server success
start proxy success
```

公网地址：`http://jenkins.frps.moe`（或查看日志中的实际地址）

## 方案二：使用LocalXpose（另一个免费内网穿透工具）

### 1. 注册LocalXpose账号
访问 https://localxpose.io/register（如果可以访问）

### 2. 下载LocalXpose客户端
```powershell
Invoke-WebRequest -Uri "https://localxpose.io/api/downloads/loclx-windows-amd64.zip" -OutFile "loclx.zip"
Expand-Archive -Path loclx.zip -DestinationPath . -Force
```

### 3. 启动LocalXpose
```bash
.\loclx.exe tunnel http --to :8090
```

## 方案三：使用GitHub Actions直接触发（不需要公网地址）

如果Jenkins可以从互联网直接访问（如通过路由器端口映射），可以跳过内网穿透。

### 配置步骤

1. **配置路由器端口映射**（可选）
   - 将路由器8090端口映射到运行Jenkins的电脑

2. **获取公网IP地址**
   ```powershell
   Invoke-RestMethod -Uri "https://api.ipify.org"
   ```

3. **在GitHub Secrets中配置**
   - **NGROK_URL**: `http://你的公网IP:8090`（或你的域名）
   - **JENKINS_USERNAME**: `hjp`
   - **JENKINS_PASSWORD**: `Hjp3494911`

## 配置GitHub Secrets

无论使用哪种方案，获取公网地址后：

1. 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions
2. 添加以下Secrets：

| Secret名称 | 示例值 |
|-----------|-------|
| NGROK_URL | http://jenkins.frps.moe（替换为实际地址） |
| JENKINS_USERNAME | hjp |
| JENKINS_PASSWORD | Hjp3494911 |

## 验证配置

1. 启动内网穿透工具
2. 访问公网地址验证Jenkins可访问
3. 推送代码到main分支
4. 检查GitHub Actions是否成功触发Jenkins构建

## 公共frp服务器信息

### 服务器1：frps.moe（免费公共服务器）
```
server_addr = 47.236.20.222
server_port = 7000
token = frp666
```

### 服务器2：frp5.cn（另一个公共服务器）
```
server_addr = 158.178.213.110
server_port = 7000
token = frp888
```

### 服务器3：备选服务器
```
server_addr = 47.251.10.87
server_port = 7000
token = freefrp123
```

## 故障排查

### frp连接失败
- 检查网络连接
- 尝试其他公共服务器
- 检查防火墙设置

### GitHub Actions无法触发Jenkins
- 确认公网地址可访问
- 检查Jenkins是否正常运行
- 验证Secrets配置是否正确