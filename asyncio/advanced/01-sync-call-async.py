import asyncio
import time


# 异步函数
async def async_operation():
    print("异步操作开始")
    await asyncio.sleep(1)  # 模拟I/O操作
    print("异步操作完成")
    return "异步结果"

"""
注意事项：
1. asyncio.run() 会创建新的事件循环，不能在已有异步上下文中使用
2. 每次从同步代码进入异步代码都有性能开销
3. 不要在异步函数内部使用这种方式，会导致嵌套事件循环问题
"""

# 同步函数中调用异步代码
def sync_function():
    print("同步函数开始")

    # 方法1: 使用asyncio.run()创建新的事件循环(Python 3.7+)
    result = asyncio.run(async_operation())
    print(f"获取到结果: {result}")

    # 方法2: 对于旧版本Python或需要更多控制的情况
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # result = loop.run_until_complete(async_operation())
    # loop.close()

    print("同步函数结束")


# 调用同步函数
sync_function()
