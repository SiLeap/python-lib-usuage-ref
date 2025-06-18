import asyncio
import threading
import queue
import time
"""
使用队列在同步和异步代码之间传递数据
将异步代码完全隔离在专用线程中
同步代码不需要变为异步
适合渐进式将同步系统迁移到异步
"""

# 异步部分
async def async_worker(task_queue, result_queue):
    while True:
        # 获取任务
        try:
            task = task_queue.get_nowait()
            if task is None:  # 结束信号
                break
        except queue.Empty:
            await asyncio.sleep(0.1)  # 避免CPU空转
            continue

        # 执行异步操作
        task_id, data = task
        print(f"异步处理任务 {task_id}")
        await asyncio.sleep(1)  # 模拟异步工作
        result = f"处理结果 {task_id}: {data} 已完成"

        # 返回结果
        result_queue.put((task_id, result))


# 异步事件循环线程
def run_async_loop(task_queue, result_queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 创建工作协程
    workers = [async_worker(task_queue, result_queue) for _ in range(3)]
    try:
        loop.run_until_complete(asyncio.gather(*workers))
    finally:
        loop.close()


# 同步部分 - 主程序
def main():
    # 创建队列用于通信
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # 启动异步处理线程
    async_thread = threading.Thread(
        target=run_async_loop,
        args=(task_queue, result_queue)
    )
    async_thread.start()

    # 提交任务
    for i in range(5):
        print(f"提交任务 {i}")
        task_queue.put((i, f"数据 {i}"))
        time.sleep(0.5)  # 模拟同步工作

    # 等待和处理结果
    results = []
    while len(results) < 5:
        try:
            result = result_queue.get_nowait()
            results.append(result)
            print(f"收到结果: {result}")
        except queue.Empty:
            time.sleep(0.1)

    # 发送结束信号并等待线程结束
    for _ in range(3):  # 为每个worker发送一个结束信号
        task_queue.put(None)
    async_thread.join()

    print("所有任务完成")


if __name__ == "__main__":
    main()
