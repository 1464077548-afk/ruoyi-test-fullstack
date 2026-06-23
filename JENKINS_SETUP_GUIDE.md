# Jenkins 本地配置指南

## 前提条件

- Jenkins 已安装并运行在 `http://localhost:8090/jenkins`
- Docker Desktop 已安装并运行
- Git 已安装
- JDK 17+ 和 Maven 已安装
- Node.js 18+ 已安装

---

## 第一步：安装必要插件

### 通过 Web UI 安装

1. 打开浏览器访问 `http://localhost:8090/jenkins`
2. 使用管理员账号登录
3. 进入 **系统管理** → **插件管理**
4. 在 "可选插件" 标签页搜索并安装以下插件：

| 插件名称 | 用途 |
|----------|------|
| Pipeline | Pipeline流水线支持 |
| HTML Publisher | HTML测试报告发布 |
| JUnit | JUnit测试结果解析 |
| Email Extension | 邮件通知 |
| Timestamper | 构建时间戳 |
| AnsiColor | 彩色日志输出 |
| Docker | Docker集成 |

### 手动安装 HTML Publisher（如需要）

如果通过Web界面安装失败，可以手动安装：

1. 下载插件: https://updates.jenkins.io/download/plugins/htmlpublisher/1.32/htmlpublisher.hpi
2. 进入 **系统管理** → **插件管理** → **高级**
3. 上传插件文件

---

## 第二步：创建 Pipeline 任务

### 方法一：通过 Web UI 创建

1. 点击 Jenkins 首页的 **新建任务**
2. 输入任务名称：`ruoyi-fullstack-test`
3. 选择 **流水线** → 点击 **确定**
4. 配置任务：

#### 基本配置
- **描述**: RuoYi全栈自动化测试CI/CD流水线

#### 构建触发器
- 勾选 **GitHub hook trigger for GITScm polling**（代码变更触发）
- 勾选 **定期构建**
- **日程表**: `H/15 * * * *`（每15分钟检查代码变更）
- 添加 **定时触发**: `0 0 * * *`（每天凌晨0点执行）

#### 流水线定义
选择 **Pipeline script from SCM**:
- **SCM**: Git
- **Repository URL**: `E:/ruoyi-ui/ruoyi_fullstack_test`
- **Credentials**: 无（本地仓库）
- **Branch Specifier**: `*/main`
- **Script Path**: `Jenkinsfile`
- **轻量级检出**: 勾选

#### 环境变量（可选）
点击 **添加环境变量**:
- `TEST_USERNAME`: `admin`
- `TEST_PASSWORD`: `admin123`

5. 点击 **保存**

### 方法二：导入配置XML

1. 将 `ci/jenkins/ruoyi-fullstack-test-config.xml` 复制到 `C:\Users\hejia\.jenkins\jobs\ruoyi-fullstack-test\config.xml`
2. 重启Jenkins服务

---

## 第三步：配置邮件通知

1. 进入 **系统管理** → **系统配置**
2. 滚动到 **Jenkins Location**
   - **Jenkins URL**: `http://localhost:8090/jenkins`
   - **系统管理员邮件地址**: `admin@example.com`

3. 滚动到 **E-mail Notification**
   - **SMTP服务器**: `smtp.example.com`
   - **用户默认邮件后缀**: `@example.com`
   - 点击 **高级**
     - 勾选 **使用SMTP认证**
     - 输入用户名和密码
     - 勾选 **使用SSL**

4. 滚动到 **Editable Email Notification**（Email Extension插件）
   - **Default Content Type**: `HTML (text/html)`
   - **Default Recipients**: `test@example.com`
   - **Enable Debug Mode**: 根据需要勾选

5. 点击 **保存**

---

## 第四步：执行构建任务

### 手动触发构建

1. 进入 `ruoyi-fullstack-test` 任务页面
2. 点击左侧 **立即构建**

### 查看构建历史

1. 进入任务页面
2. 点击 **构建历史**
3. 选择具体构建编号查看详情

### 查看控制台输出

1. 点击构建编号
2. 点击左侧 **控制台输出**

### 查看测试报告

构建完成后：
1. 点击构建编号
2. 在左侧菜单中：
   - **HTML Report**: 查看HTML格式的测试报告
   - **Test Result**: 查看JUnit格式的测试结果
3. 点击 **工作区** 可以查看构建产物

---

## 第五步：配置触发条件

### 代码变更触发

1. 进入任务配置
2. 在 **构建触发器** 部分：
   - 勾选 **轮询SCM**
   - 在 **日程表** 中输入: `H/15 * * * *`

### 定时触发（每日凌晨）

1. 在任务配置中：
   - 勾选 **定期构建**
   - 在 **日程表** 中输入: `0 0 * * *`

### GitHub Webhook 触发（可选）

1. 在GitHub仓库设置中添加webhook:
   - Payload URL: `http://your-jenkins-url/github-webhook/`
   - Content type: `application/json`
   - Events: 选择 `push` 和 `pull request`

---

## 第六步：Docker配置（如需要）

### Windows Docker 配置

如果Jenkins运行在Windows上，需要配置Docker：

1. 安装 Docker Desktop for Windows
2. 启用 **Expose daemon on tcp://localhost:2375**
3. 在Jenkins任务中添加环境变量：
   ```
   DOCKER_HOST=tcp://localhost:2375
   ```

### Linux Docker 配置

如果Jenkins运行在Linux上：

1. 将Jenkins用户添加到docker组：
   ```bash
   sudo usermod -aG docker jenkins
   ```
2. 重启Jenkins服务

---

## 故障排除

### 构建失败：找不到Docker命令

**问题**: `docker-compose: command not found`

**解决**:
1. 确保Docker Desktop已安装并运行
2. 在Jenkins系统配置中配置Docker路径
3. 或者在Pipeline中使用完整路径

### 构建失败：端口被占用

**问题**: `port is already allocated`

**解决**:
1. 检查端口占用：`netstat -ano | findstr ":8080"`
2. 修改 `.env` 文件中的端口映射
3. 或者停止占用端口的服务

### 测试失败：服务启动超时

**问题**: `服务启动超时`

**解决**:
1. 增加等待时间：`sleep 300`（5分钟）
2. 检查Docker日志：`docker-compose logs`
3. 确保机器有足够的资源（内存、CPU）

### 报告无法显示

**问题**: HTML报告404

**解决**:
1. 确保HTML Publisher插件已安装
2. 检查报告路径是否正确
3. 确保Jenkins用户有读取权限

### 邮件发送失败

**问题**: `javax.mail.AuthenticationFailedException`

**解决**:
1. 检查SMTP配置是否正确
2. 确保邮箱开启了SMTP服务
3. 使用应用专用密码而非邮箱登录密码

---

## 快速参考

### 常用Jenkins URL

| 用途 | URL |
|------|-----|
| Jenkins首页 | http://localhost:8090/jenkins |
| 插件管理 | http://localhost:8090/jenkins/pluginManager |
| 系统配置 | http://localhost:8090/jenkins/configure |
| 构建历史 | http://localhost:8090/jenkins/job/ruoyi-fullstack-test/buildHistory |
| 新建任务 | http://localhost:8090/jenkins/view/all/newJob |

### 常用Pipeline命令

```groovy
// 触发下游任务
build '下游任务名称'

// 发送邮件
emailext subject: '测试', body: '内容', to: 'test@example.com'

// 归档文件
archiveArtifacts artifacts: 'reports/**/*'

// 发布HTML报告
publishHTML target: [
    reportDir: 'reports/html',
    reportFiles: '*.html',
    reportName: '测试报告'
]
```

### Cron表达式示例

| 表达式 | 含义 |
|--------|------|
| `H/15 * * * *` | 每15分钟 |
| `H H(0-8) * * *` | 每天0-8点之间的任意时间 |
| `0 0 * * *` | 每天凌晨0点 |
| `0 0 * * 1-5` | 工作日凌晨0点 |
| `0 0 1 * *` | 每月1日凌晨0点 |

---

## 配置文件位置

| 文件 | 说明 |
|------|------|
| `Jenkinsfile` | Pipeline脚本主文件 |
| `ci/jenkins/ruoyi-fullstack-test-config.xml` | 任务配置XML |
| `ci/jenkins/Jenkinsfile` | Jenkins Pipeline配置备份 |
| `docker-compose.yml` | Docker服务编排 |
| `.env` | 环境变量配置 |

---

## 下一步

1. 确保RuoYi-Vue源码在 `E:/ruoyi-ui/RuoYi-Vue` 目录
2. 确保测试代码在 `E:/ruoyi-ui/ruoyi_fullstack_test` 目录
3. 运行 `./start-services.bat` 启动本地服务
4. 在Jenkins中点击 **立即构建** 测试流水线
