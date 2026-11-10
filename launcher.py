#!/usr/bin/env python3
"""拨测工具启动菜单。

入口脚本（start.sh / start.bat / start.ps1）只负责找到 Python 并执行本文件，
菜单、启动服务器、结束进程等逻辑全部在这里实现。
"""

import os
import signal
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(BASE_DIR, "phone_dial_checker.py")
PORT = 8765
MARKER = "phone_dial_checker.py"


def list_server_pids():
    """返回正在运行 phone_dial_checker.py 的进程号（排除当前进程）。"""
    me = os.getpid()
    if os.name == "nt":
        cmd = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.Name -match '^(python|py)(w)?\\.exe$' -and "
            "$_.CommandLine -like '*phone_dial_checker.py*' } | "
            "ForEach-Object { $_.ProcessId }"
        )
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True, timeout=15,
            )
        except (OSError, subprocess.SubprocessError):
            return []
        return [int(x) for x in out.stdout.split() if x.isdigit() and int(x) != me]
    pids = []
    proc_root = "/proc"
    if os.path.isdir(proc_root):
        for name in os.listdir(proc_root):
            if not name.isdigit():
                continue
            try:
                with open(os.path.join(proc_root, name, "cmdline"), "rb") as f:
                    parts = f.read().decode("utf-8", "ignore").split("\0")
            except OSError:
                continue
            # 只认 Python 解释器启动的进程，避免误杀命令行中恰好提到脚本名的 shell/编辑器
            if not parts or not os.path.basename(parts[0]).lower().startswith("python"):
                continue
            if any(os.path.basename(p) == MARKER for p in parts[1:]):
                pids.append(int(name))
    return [p for p in pids if p != me]


def start_server():
    if not os.path.isfile(SERVER):
        print("未找到服务器脚本: %s" % SERVER)
        return
    os.chdir(BASE_DIR)
    print("启动服务器，端口 %d（按 Ctrl+C 退出）..." % PORT)
    sys.stdout.flush()
    os.execv(sys.executable, [sys.executable, SERVER])


def stop_server():
    pids = list_server_pids()
    if not pids:
        print("未发现运行中的服务器。")
        return
    for pid in pids:
        print("正在结束进程 %d ..." % pid)
        try:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            else:
                os.kill(pid, signal.SIGTERM)
        except OSError as exc:
            print("结束进程 %d 失败: %s" % (pid, exc))
    deadline = time.time() + 5
    while time.time() < deadline:
        if not set(pids) & set(list_server_pids()):
            break
        time.sleep(0.2)
    else:
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
    print("服务器已停止。")


def main():
    print("手机号拨测工具")
    print("  1) 启动服务器")
    print("  2) 结束服务器进程")
    try:
        choice = input("请选择 [1/2]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    if choice == "1":
        start_server()
    elif choice == "2":
        stop_server()
    else:
        print("无效选择: %s" % choice)


if __name__ == "__main__":
    main()
