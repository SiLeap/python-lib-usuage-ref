import subprocess

# 捕获标准输出
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(f"标准输出:\n{result.stdout}")

# 捕获标准错误
result = subprocess.run(['ls', 'non_existent_file'],
                        capture_output=True,
                        text=True)
print(f"标准错误:\n{result.stderr}")

# 同时捕获标准输出和标准错误
result = subprocess.run(['ls', '-l', 'non_existent_file'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True)
print(f"标准输出:\n{result.stdout}")
print(f"标准错误:\n{result.stderr}")
