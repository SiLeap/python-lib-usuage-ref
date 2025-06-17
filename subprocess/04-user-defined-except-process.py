import subprocess
import sys

def execute_command(cmd, timeout=None):
    """执行命令并提供友好的错误处理"""
    try:
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              check=True,
                              timeout=timeout)
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': f"找不到命令: {cmd[0]}",
            'error_type': 'command_not_found'
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': f"命令返回非零状态码: {e.returncode}",
            'stdout': e.stdout,
            'stderr': e.stderr,
            'returncode': e.returncode,
            'error_type': 'non_zero_exit'
        }
    except subprocess.TimeoutExpired as e:
        return {
            'success': False,
            'error': f"命令执行超时: {timeout}秒",
            'error_type': 'timeout'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"执行命令时发生未知错误: {e}",
            'error_type': 'unknown'
        }

# 测试
result = execute_command(['ls', '-l'])
if result['success']:
    print(f"命令输出:\n{result['stdout']}")
else:
    print(f"错误: {result['error']}")
