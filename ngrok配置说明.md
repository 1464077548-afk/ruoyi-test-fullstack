# ngrok认证配置说明

## 问题
ngrok显示 "reconnecting (failed to send authentication request)"，需要配置认证token。

## 解决方案

### 1. 注册ngrok账号

访问 https://ngrok.com/signup 注册免费账号

### 2. 获取Auth Token

登录后在Dashboard中复制你的authtoken：
- 访问：https://dashboard.ngrok.com/get-started/your-authtoken

### 3. 配置authtoken

在命令行中运行：
```bash
ngrok.exe config add-authtoken YOUR_AUTH_TOKEN
```

将 `YOUR_AUTH_TOKEN` 替换为你在ngrok网站获取的实际token。

### 4. 重新启动ngrok

```bash
.\ngrok.exe http 8090
```

## 验证

启动成功后应该显示：
```
Session Status                online
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8090
```

## 使用ngrok地址

获取到公网地址后（如 https://abc123.ngrok.io），需要：

1. **配置GitHub Secrets**
   - 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/secrets/actions
   - 添加 `NGROK_URL` = `https://abc123.ngrok.io`（替换为实际地址）

2. **配置GitHub Webhook（可选）**
   - 访问：https://github.com/1464077548-afk/ruoyi-test-fullstack/settings/hooks
   - Payload URL: `https://abc123.ngrok.io/generic-webhook-trigger/invoke`

## 注意事项

- 免费版ngrok每次重启会更换地址
- 如果需要固定地址，需要升级到付费版
- 保持ngrok运行才能接收GitHub的Webhook请求