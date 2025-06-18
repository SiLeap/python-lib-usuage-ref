import asyncio


class AsyncContextManager:
    async def __aenter__(self):
        print("Entering context")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        await asyncio.sleep(1)


async def main():
    async with AsyncContextManager() as manager:
        print("Inside context")


asyncio.run(main())
