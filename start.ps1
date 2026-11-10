# 手机号拨测工具入口脚本：仅负责找到 Python 并运行 launcher.py
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) {
    & py -3 launcher.py
    exit $LASTEXITCODE
}

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & python launcher.py
    exit $LASTEXITCODE
}

Write-Host "[错误] 未找到 Python 3，请先安装后重试" -ForegroundColor Red
exit 1
