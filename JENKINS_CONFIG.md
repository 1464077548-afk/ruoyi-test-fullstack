# Jenkins 自动化测试集成配置指南

## 概述
本指南说明如何在 Jenkins 中配置 ruoyi_fullstack_test 自动化测试任务，实现每天晚上9点自动执行测试并生成报告。

---

## 环境要求
- Jenkins 已安装并运行
- 已安装以下 Jenkins 插件：
  - Pipeline (流水线插件)
  - HTML Publisher (HTML报告发布)
  - JUnit (测试结果解析)
  - NodeJS (如需要)

---

## 配置方法一：使用 Pipeline 流水线（推荐）

### 步骤1：安装必要插件
1. 登录 Jenkins → 管理 Jenkins → 插件管理
2. 安装以下插件：
   - Pipeline
   - HTML Publisher
   - JUnit

### 步骤2：创建 Pipeline 任务
1. 点击「新建任务」
2. 输入任务名称：`ruoyi-fullstack-test`
3. 选择「流水线」→ 点击「确定」

### 步骤3：配置任务
#### 基本配置
- **描述**: RuoYi 全栈自动化测试

#### 构建触发器
- 勾选「Build periodically」
- **日程表**: `0 21 * * *`
  - 含义：每天晚上 21:00 执行

#### 流水线定义
- 选择「Pipeline script from SCM」
- **SCM**: Git
- **Repository URL**: 你的代码仓库地址
- **Credentials**: 配置 Git 凭证
- **Branch Specifier**: `*/main` 或你的分支
- **Script Path**: `Jenkinsfile`

### 步骤4：保存并测试
点击「保存」后，点击「立即构建」测试配置是否正确。

---

## 配置方法二：使用自由风格任务

### 步骤1：创建自由风格任务
1. 点击「新建任务」
2. 输入任务名称：`ruoyi-fullstack-test`
3. 选择「自由风格软件项目」→ 点击「确定」

### 步骤2：配置任务
#### 基本配置
- **描述**: RuoYi 全栈自动化测试

#### 构建触发器
- 勾选「Build periodically」
- **日程表**: `0 21 * * *`

#### 构建环境
- 勾选「Delete workspace before build starts」

#### 构建
点击「添加构建步骤」→ 选择「执行 Windows 批处理命令」

```batch
cd E:\ruoyi-ui\ruoyi_fullstack_test
run_tests.bat
```

#### 构建后操作
1. **Publish HTML reports**
   - HTML directory to archive: `reports/html`
   - Index page[s]: `report.html`
   - Report title: `自动化测试报告`

2. **Publish JUnit test result report**
   - Test report XMLs: `reports/junit/*.xml`

### 步骤3：保存并测试
点击「保存」后，点击「立即构建」测试配置是否正确。

---

## 手动运行测试

如果需要手动运行测试，可直接执行：

```batch
cd E:\ruoyi-ui\ruoyi_fullstack_test
run_tests.bat
```

---

## Cron 表达式说明

| 字段 | 说明 | 允许值 |
|------|------|--------|
| 分钟 | 分钟数 | 0-59 |
| 小时 | 小时数 | 0-23 |
| 日期 | 日期 | 1-31 |
| 月份 | 月份 | 1-12 |
| 星期 | 星期几 | 0-7 (0和7表示周日) |

**示例**:
- `0 21 * * *` - 每天晚上 21:00
- `0 9,18 * * *` - 每天早上9点和晚上6点
- `0 0 * * 1` - 每周一凌晨0点

---

## 测试报告位置

测试执行完成后，报告将保存在：
- HTML 报告: `E:\ruoyi-ui\ruoyi_fullstack_test\reports\html\report.html`
- JUnit XML: `E:\ruoyi-ui\ruoyi_fullstack_test\reports\junit\`

在 Jenkins 中可通过「自动化测试报告」链接查看。

---

## 故障排除

### 常见问题

1. **测试脚本执行失败**
   - 检查 Python 环境是否正确配置
   - 确保已安装所有依赖包
   - 检查 Playwright 浏览器是否安装

2. **报告无法显示**
   - 确保 HTML Publisher 插件已安装
   - 检查报告路径配置是否正确

3. **构建权限问题**
   - 确保 Jenkins 用户对测试目录有读写权限
   - 检查 `E:\ruoyi-ui\ruoyi_fullstack_test` 目录权限

4. **定时任务不执行**
   - 检查 Jenkins 系统时间是否正确
   - 确认 Cron 表达式格式正确
   - 检查 Jenkins 日志排查问题

---

## 相关文件

- `Jenkinsfile` - Pipeline 流水线配置
- `run_tests.bat` - Windows 测试执行脚本
- `requirements.txt` - Python 依赖列表