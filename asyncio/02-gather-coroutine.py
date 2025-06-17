import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return f"{what} done"

# 注意虽然有两个等待时间（1秒和2秒），但总执行时间约为2秒，因为协程是并发执行的。
async def main():
    start = time.time()

    # 并发执行多个协程
    results = await asyncio.gather(
        say_after(1, "hello"),
        say_after(2, "world")
    )

    end = time.time()
    print(f"Completed in {end - start:.2f} seconds")
    print(f"Results: {results}")


asyncio.run(main())
