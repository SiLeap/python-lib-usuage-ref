import subprocess
import resource
import os


def set_resource_limits():
    """设置资源限制"""
    # 限制 CPU 时间 (秒)
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

    # 限制内存使用 (字节)
    resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))

    # 限制创建的进程数
    resource.setrlimit(resource.RLIMIT_NPROC, (5, 5))


# 使用资源限制运行一个进程
# 注意: 这个函数需要在 Unix/Linux 系统上运行
def run_with_resource_limits(cmd):
    """使用资源限制运行命令"""
    try:
        process = subprocess.Popen(cmd,
                                   preexec_fn=set_resource_limits,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        stdout, stderr = process.communicate()
        return {
            'returncode': process.returncode,
            'stdout': stdout,
            'stderr': stderr
        }
    except Exception as e:
        return {
            'error': str(e)
        }


# 测试资源限制
result = run_with_resource_limits(['python', '-c',
                                   'import time; print("Starting"); time.sleep(2); print("Finished")'])
print(f"返回码: {result.get('returncode')}")
print(f"标准输出: {result.get('stdout')}")
print(f"标准错误: {result.get('stderr')}")
print(f"错误: {result.get('error', 'None')}")
