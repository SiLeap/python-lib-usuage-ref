import asyncio
import random


async def producer(queue, id):
    for i in range(5):
        value = random.randint(1, 100)
        await queue.put(value)
        print(f"Producer {id} produced: {value}")
        await asyncio.sleep(random.random())


async def consumer(queue, id):
    while True:
        value = await queue.get()
        print(f"Consumer {id} got: {value}")
        await asyncio.sleep(random.random())
        queue.task_done()  # 通知队列任务完成


async def main():
    queue = asyncio.Queue(maxsize=5)  # 限制队列大小

    # 创建 3 个生产者和 2 个消费者
    producers = [producer(queue, i) for i in range(3)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(2)]

    # 等待所有生产者完成
    await asyncio.gather(*producers)

    # 等待队列中所有项目被处理
    await queue.join()

    # 取消所有消费者
    for c in consumers:
        c.cancel()


asyncio.run(main())
