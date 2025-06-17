import subprocess

# 通过 input 参数提供输入
result = subprocess.run(['grep', 'hello'],
                        input="hello world\ngoodbye world",
                        capture_output=True,
                        text=True)
print(f"匹配行: {result.stdout}")

# 使用 Popen 和 communicate 提供输入
process = subprocess.Popen(['sort'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          text=True)
stdout, stderr = process.communicate(input="banana\napple\ncherry")
print(f"排序结果:\n{stdout}")
