import subprocess
import sys
import os


def run_windows_command():
    """Windows 平台特定的子进程处理"""
    if sys.platform != 'win32':
        print("这个示例只在 Windows 上运行")
        return

    # 在 Windows 上，可以直接使用命令名而不需要完整路径
    result = subprocess.run('dir',
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result.stdout)

    # 使用 start 命令打开文件
    subprocess.run(['start', 'notepad'], shell=True)

    # 使用 tasklist 获取进程列表
    result = subprocess.run('tasklist /FI "IMAGENAME eq python.exe"',
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result.stdout)

    # 静默运行命令 (隐藏控制台窗口)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE
    result = subprocess.run(['ping', 'localhost'],
                            startupinfo=startupinfo,
                            capture_output=True,
                            text=True)
    print(result.stdout)


# 仅在 Windows 上运行
if sys.platform == 'win32':
    print("运行 Windows 特定命令:")
    run_windows_command()
else:
    print("当前平台不是 Windows，跳过 Windows 特定示例")
