import subprocess

# 用于执行命令的高级函数
# 基本用法
result = subprocess.run(['echo', 'Hello World'])

# 捕获输出
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(result.stdout)

# 设置超时
try:
    result = subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired:
    print("命令执行超时")

# 检查命令是否成功执行
try:
    result = subprocess.run(['ls', 'non_existent_file'], check=True)
except subprocess.CalledProcessError as e:
    print(f"命令执行失败: {e}")

# Popen 是一个更底层的接口，提供更细粒度的控制
# 创建进程
process = subprocess.Popen(['echo', 'Hello World'],
                           stdout=subprocess.PIPE,
                           text=True)
# 获取输出
stdout, stderr = process.communicate()
print(f"输出: {stdout}")
# 获取返回码
return_code = process.returncode
print(f"返回码: {return_code}")