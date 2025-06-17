import subprocess
import select
import time


def monitor_multiple_processes(commands, timeout=60):
    """同时监控多个进程的输出"""
    processes = []

    # 启动所有命令
    for i, cmd in enumerate(commands):
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   bufsize=1)
        processes.append({
            'process': process,
            'cmd': cmd,
            'index': i,
            'stdout_lines': [],
            'stderr_lines': []
        })

    # 监控所有进程的输出
    start_time = time.time()
    remaining_processes = len(processes)

    while remaining_processes > 0 and (time.time() - start_time) < timeout:
        # 收集所有要监控的文件描述符
        read_fds = []
        fd_to_process = {}

        for p in processes:
            process = p['process']
            if process.poll() is None:  # 进程仍在运行
                if process.stdout:
                    read_fds.append(process.stdout)
                    fd_to_process[process.stdout.fileno()] = (p, 'stdout')
                if process.stderr:
                    read_fds.append(process.stderr)
                    fd_to_process[process.stderr.fileno()] = (p, 'stderr')

        if not read_fds:
            break  # 没有活动的文件描述符

        # 使用 select 等待有数据可读的文件描述符
        readable, _, _ = select.select(read_fds, [], [], 0.1)

        for fd in readable:
            p, stream_name = fd_to_process[fd.fileno()]
            line = fd.readline()
            if line:
                line = line.strip()
                if stream_name == 'stdout':
                    p['stdout_lines'].append(line)
                    print(f"进程 {p['index']} ({' '.join(p['cmd'])}) stdout: {line}")
                else:
                    p['stderr_lines'].append(line)
                    print(f"进程 {p['index']} ({' '.join(p['cmd'])}) stderr: {line}")

        # 检查是否有进程已结束
        for p in processes:
            if p['process'].poll() is not None and 'exit_code' not in p:
                p['exit_code'] = p['process'].returncode
                print(f"进程 {p['index']} ({' '.join(p['cmd'])}) 已结束，返回码: {p['exit_code']}")
                remaining_processes -= 1

        time.sleep(0.01)  # 避免 CPU 占用过高

    # 确保所有进程都已结束
    for p in processes:
        if 'exit_code' not in p:
            if p['process'].poll() is None:
                p['process'].terminate()
                p['process'].wait(timeout=2)
                p['exit_code'] = p['process'].returncode
                print(f"进程 {p['index']} ({' '.join(p['cmd'])}) 被终止，返回码: {p['exit_code']}")

    return processes


# 测试同时监控多个进程
commands = [
    ['bash', '-c', 'for i in {1..3}; do echo "Process 1: $i"; sleep 1; done'],
    ['bash', '-c', 'for i in {1..5}; do echo "Process 2: $i"; sleep 0.5; done'],
    ['bash', '-c', 'for i in {1..2}; do echo "Process 3: $i"; echo "Error in 3" >&2; sleep 1; done']
]

print("开始监控多个进程:")
results = monitor_multiple_processes(commands)

# 打印汇总信息
print("\n结果汇总:")
for p in results:
    print(f"进程 {p['index']} ({' '.join(p['cmd'])}):")
    print(f"  返回码: {p['exit_code']}")
    print(f"  stdout 行数: {len(p['stdout_lines'])}")
    print(f"  stderr 行数: {len(p['stderr_lines'])}")
