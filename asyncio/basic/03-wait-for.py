import asyncio

async def long_operation():
    await asyncio.sleep(5)
    return "Operation completed"

async def main():
    try:
        # 设置 3 秒超时
        result = await asyncio.wait_for(long_operation(), timeout=3)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")

asyncio.run(main())
