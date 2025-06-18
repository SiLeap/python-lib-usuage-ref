import asyncio
import time
import concurrent.futures

"""
run_in_executor 允许在不阻塞事件循环的情况下执行同步代码
对IO密集型任务使用 ThreadPoolExecutor
对CPU密集型任务使用 ProcessPoolExecutor
记住：虽然同步代码被隔离执行，但仍会消耗资源
"""
# 模拟耗时的同步操作
def blocking_io():
    print(f"开始阻塞IO操作 - 线程ID: {threading.get_ident()}")
    time.sleep(2)  # 模拟文件IO
    print(f"阻塞IO操作完成 - 线程ID: {threading.get_ident()}")
    return "IO结果"


def cpu_bound():
    print(f"开始CPU密集操作 - 线程ID: {threading.get_ident()}")
    # 计算密集型操作
    result = sum(i * i for i in range(10 ** 7))
    print(f"CPU密集操作完成 - 线程ID: {threading.get_ident()}")
    return result


async def main():
    print(f"主异步函数 - 线程ID: {threading.get_ident()}")

    # 方法1: 使用线程池执行IO密集型同步代码
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result1 = await loop.run_in_executor(pool, blocking_io)
        print(f"IO结果: {result1}")

    # 方法2: 使用进程池执行CPU密集型同步代码
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result2 = await loop.run_in_executor(pool, cpu_bound)
        print(f"CPU结果: {result2}")

    # 同时也可以继续执行普通的异步操作
    await asyncio.sleep(1)
    print("其他异步操作完成")


import threading

print(f"程序开始 - 主线程ID: {threading.get_ident()}")
asyncio.run(main())
print("程序结束")
