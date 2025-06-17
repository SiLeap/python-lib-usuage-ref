import subprocess
import threading
import time


def stream_output(process, stream_name):
    """实时流式处理进程输出"""
    stream = process.stdout if stream_name == 'stdout' else process.stderr
    for line in iter(stream.readline, ''):
        if not line:
            break
        print(f"{stream_name}: {line.strip()}")


def run_with_live_output(cmd):
    """运行命令并实时显示输出"""
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               bufsize=1)

    # 创建线程来处理输出流
    stdout_thread = threading.Thread(target=stream_output,
                                     args=(process, 'stdout'))
    stderr_thread = threading.Thread(target=stream_output,
                                     args=(process, 'stderr'))

    # 设置为守护线程，当主线程退出时，这些线程也会退出
    stdout_thread.daemon = True
    stderr_thread.daemon = True

    # 启动线程
    stdout_thread.start()
    stderr_thread.start()

    # 等待进程完成
    return_code = process.wait()

    # 等待线程完成
    stdout_thread.join()
    stderr_thread.join()

    return return_code


# 测试实时输出
print("运行命令并实时显示输出:")
return_code = run_with_live_output(['bash', '-c',
                                    'for i in {1..5}; do echo "Line $i"; sleep 1; done; echo "Error line" >&2'])
print(f"命令结束，返回码: {return_code}")
