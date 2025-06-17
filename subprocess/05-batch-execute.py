import subprocess
import concurrent.futures


def run_command(cmd):
    """执行单个命令并返回结果"""
    try:
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                check=True)
        return {
            'cmd': cmd,
            'success': True,
            'output': result.stdout
        }
    except Exception as e:
        return {
            'cmd': cmd,
            'success': False,
            'error': str(e)
        }


def batch_execute(commands, max_workers=5):
    """并行执行多个命令"""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有命令
        future_to_cmd = {executor.submit(run_command, cmd): cmd for cmd in commands}

        # 获取结果
        for future in concurrent.futures.as_completed(future_to_cmd):
            results.append(future.result())

    return results


# 测试批量执行
commands = [
    ['echo', 'Hello World'],
    ['ls', '-l'],
    ['date'],
    ['whoami'],
    ['non_existent_command']  # 这个会失败
]

results = batch_execute(commands)

# 打印结果
for result in results:
    if result['success']:
        print(f"命令 {result['cmd']} 成功: {result['output'].strip()}")
    else:
        print(f"命令 {result['cmd']} 失败: {result['error']}")
