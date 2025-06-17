import asyncio


async def increment_with_lock(lock, counter, delay):
    async with lock:  # 确保同一时间只有一个协程能修改 counter
        current = counter[0]
        await asyncio.sleep(delay)  # 模拟耗时操作
        counter[0] = current + 1
        print(f"Counter incremented to {counter[0]}")


async def main():
    counter = [0]
    lock = asyncio.Lock()

    # 同时启动多个协程修改同一个计数器
    await asyncio.gather(
        increment_with_lock(lock, counter, 0.1),
        increment_with_lock(lock, counter, 0.2),
        increment_with_lock(lock, counter, 0.1)
    )

    print(f"Final counter value: {counter[0]}")


asyncio.run(main())
