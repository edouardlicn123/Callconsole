@echo off
rem 手机号拨测工具入口脚本：仅负责找到 Python 并运行 launcher.py
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>&1 && (
    py -3 launcher.py
    exit /b
)
where python >nul 2>&1 && (
    python launcher.py
    exit /b
)

echo [错误] 未找到 Python 3，请先安装后重试
exit /b 1
