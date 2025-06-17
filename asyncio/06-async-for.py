import asyncio


class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.counter = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.counter < self.limit:
            self.counter += 1
            await asyncio.sleep(0.1)  # 模拟异步操作
            return self.counter
        raise StopAsyncIteration


async def async_range(start, stop):
    for i in range(start, stop):
        await asyncio.sleep(0.1)  # 模拟异步操作
        yield i


async def main():
    async for number in AsyncCounter(5):
        print(number)
    async for number in async_range(1, 6):
        print(number)


asyncio.run(main())
