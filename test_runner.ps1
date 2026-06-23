$env:TEST_DIR = "E:\ruoyi-ui\ruoyi_fullstack_test"
$env:VENV_PYTHON = "$env:TEST_DIR\venv\Scripts\python.exe"
$env:REPORT_DIR = "$env:TEST_DIR\reports"

Write-Host "检查测试目录..."
if (-not (Test-Path $env:TEST_DIR)) {
    Write-Host "错误: 测试目录不存在: $env:TEST_DIR"
    exit 1
}
Write-Host "测试目录: $env:TEST_DIR"

Write-Host "检查虚拟环境Python..."
if (-not (Test-Path $env:VENV_PYTHON)) {
    Write-Host "错误: 虚拟环境Python不存在: $env:VENV_PYTHON"
    exit 1
}
Write-Host "使用Python: $env:VENV_PYTHON"

Write-Host "创建报告目录..."
New-Item -ItemType Directory -Path "$env:REPORT_DIR\html" -Force | Out-Null

Write-Host "开始运行测试..."
& "$env:VENV_PYTHON" -m pytest tests/ -v --tb=short --html="$env:REPORT_DIR\html\report.html" --self-contained-html

$TEST_RESULT = $LASTEXITCODE

if ($TEST_RESULT -eq 0) {
    Write-Host "自动化测试执行成功！"
} else {
    Write-Host "自动化测试执行失败，退出码: $TEST_RESULT"
}

exit $TEST_RESULT