import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# 在 Python 3.7+ 中使用
if __name__ == "__main__":
    asyncio.run(main())
