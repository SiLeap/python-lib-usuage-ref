import subprocess
import os


def run_with_nice(cmd, nice_level=10):
    """使用指定的 nice 值运行命令"""
    # nice 值范围: -20 (最高优先级) 到 19 (最低优先级)
    # 普通用户只能增加 nice 值 (降低优先级)

    # 方法1: 使用 nice 命令
    nice_cmd = ['nice', f'-n{nice_level}'] + cmd
    return subprocess.run(nice_cmd, capture_output=True, text=True)

    # 方法2: 使用 os.setpriority (仅在 Unix 系统上有效)
    # def set_priority():
    #     os.setpriority(os.PRIO_PROCESS, 0, nice_level)
    #
    # return subprocess.run(cmd, preexec_fn=set_priority, capture_output=True, text=True)


# 测试不同优先级
print("正常优先级:")
normal_result = subprocess.run(['bash', '-c', 'echo $$ && nice'],
                               capture_output=True,
                               text=True)
print(normal_result.stdout)

print("\n低优先级:")
low_result = run_with_nice(['bash', '-c', 'echo $$ && nice'], 10)
print(low_result.stdout)
