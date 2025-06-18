import asyncio


async def cancelable_operation():
    try:
        while True:
            print("Working...")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("Operation was cancelled")
        raise  # 重新抛出异常以便正确清理


async def main():
    task = asyncio.create_task(cancelable_operation())

    # 让任务运行一段时间
    await asyncio.sleep(2)

    # 取消任务
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Main: task was cancelled")


asyncio.run(main())
