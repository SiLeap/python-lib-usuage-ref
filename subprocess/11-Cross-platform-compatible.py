import subprocess
import sys
import os


def open_file(filepath):
    """跨平台打开文件"""
    if sys.platform == 'win32':
        # Windows
        os.startfile(filepath)
    elif sys.platform == 'darwin':
        # macOS
        subprocess.run(['open', filepath])
    else:
        # Linux/Unix
        subprocess.run(['xdg-open', filepath])


def get_platform_specific_command(cmd_type):
    """获取跨平台命令"""
    commands = {
        'list_dir': {
            'win32': ['dir'],
            'default': ['ls', '-la']
        },
        'list_processes': {
            'win32': ['tasklist'],
            'darwin': ['ps', '-ax'],
            'default': ['ps', '-ef']
        },
        'find_file': {
            'win32': ['where'],
            'default': ['which']
        }
    }

    platform_cmds = commands.get(cmd_type, {})
    return platform_cmds.get(sys.platform, platform_cmds.get('default', []))


# 测试跨平台命令
print(f"当前平台: {sys.platform}")

list_dir_cmd = get_platform_specific_command('list_dir')
print(f"列目录命令: {list_dir_cmd}")
result = subprocess.run(list_dir_cmd,
                        shell=(sys.platform == 'win32'),
                        capture_output=True,
                        text=True)
print(f"命令输出 (前5行):\n{''.join(result.stdout.splitlines(True)[:5])}")

list_proc_cmd = get_platform_specific_command('list_processes')
print(f"\n列进程命令: {list_proc_cmd}")
result = subprocess.run(list_proc_cmd,
                        shell=(sys.platform == 'win32'),
                        capture_output=True,
                        text=True)
print(f"命令输出 (前5行):\n{''.join(result.stdout.splitlines(True)[:5])}")
