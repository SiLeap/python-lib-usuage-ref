import asyncio


async def waiter(event):
    print("Waiting for event...")
    await event.wait()
    print("Event received, continuing")


async def setter(event, delay):
    await asyncio.sleep(delay)
    print("Setting event...")
    event.set()


async def main():
    event = asyncio.Event()

    # 同时启动 waiter 和 setter
    await asyncio.gather(
        waiter(event),
        setter(event, 2)
    )


asyncio.run(main())
