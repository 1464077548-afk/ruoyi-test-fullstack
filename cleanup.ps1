# 清理测试项目中的大文件和缓存
Write-Host "开始清理测试项目..." -ForegroundColor Green

# 清理 Playwright 视频录制文件
if (Test-Path "recordings") {
    Write-Host "正在清理 recordings 目录..." -ForegroundColor Yellow
    Get-ChildItem -Path "recordings" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path "recordings" -Directory -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Write-Host "✅ recordings 目录已清理" -ForegroundColor Green
}

# 清理 pytest 缓存
if (Test-Path ".pytest_cache") {
    Write-Host "正在清理 pytest 缓存..." -ForegroundColor Yellow
    Get-ChildItem -Path ".pytest_cache" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Write-Host "✅ pytest 缓存已清理" -ForegroundColor Green
}

# 清理 __pycache__
Write-Host "正在清理 Python 缓存..." -ForegroundColor Yellow
Get-ChildItem -Path "." -Include "__pycache__" -Recurse -Directory | ForEach-Object {
    Remove-Item $_.FullName -Force -Recurse -ErrorAction SilentlyContinue
}
Write-Host "✅ Python 缓存已清理" -ForegroundColor Green

# 清理截图文件
Write-Host "正在清理截图文件..." -ForegroundColor Yellow
Get-ChildItem -Path "." -Include "*.png" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✅ 截图文件已清理" -ForegroundColor Green

# 清理 HTML 报告（保留最新3个）
Write-Host "正在清理旧报告..." -ForegroundColor Yellow
if (Test-Path "reports\html") {
    $reports = Get-ChildItem -Path "reports\html" -Filter "report.html" | Sort-Object LastWriteTime -Descending
    if ($reports.Count -gt 3) {
        $reports | Select-Object -Skip 3 | Remove-Item -Force
        Write-Host "✅ 已保留最新3个报告，删除了 $($reports.Count - 3) 个旧报告" -ForegroundColor Green
    }
}

# 统计清理后的空间
Write-Host "`n清理完成！当前项目大小：" -ForegroundColor Cyan
$totalSize = (Get-ChildItem -Path "." -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)
$totalSizeGB = [math]::Round($totalSize / 1GB, 2)
Write-Host "总大小: $totalSizeMB MB ($totalSizeGB GB)" -ForegroundColor Cyan

# 磁盘空间信息
Write-Host "`n磁盘空间信息：" -ForegroundColor Cyan
Get-PSDrive -Name C | Select-Object Name, @{Name="Used(GB)";Expression={[math]::Round($_.Used/1GB,2)}}, @{Name="Free(GB)";Expression={[math]::Round($_.Free/1GB,2)}}, @{Name="Total(GB)";Expression={[math]::Round(($_.Used+$_.Free)/1GB,2)}} | Format-Table -AutoSize

Write-Host "`n✅ 清理完成！现在可以重新运行测试了。" -ForegroundColor Green
