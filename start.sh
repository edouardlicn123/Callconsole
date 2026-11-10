#!/usr/bin/env bash
# 手机号拨测工具入口脚本：仅负责找到 Python 并运行 launcher.py
cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
    exec python3 launcher.py
fi
if command -v python >/dev/null 2>&1; then
    exec python launcher.py
fi

echo "[错误] 未找到 Python 3，请先安装后重试" >&2
exit 1
