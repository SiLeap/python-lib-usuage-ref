import asyncio
from aiohttp import web


async def handle(request):
    await asyncio.sleep(0.5)  # 模拟处理时间
    name = request.match_info.get('name', "Anonymous")
    return web.Response(text=f"Hello, {name}!")


async def main():
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        web.get('/{name}', handle)
    ])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)

    print("Server started at http://localhost:8080")
    await site.start()

    # 保持服务器运行
    try:
        await asyncio.Future()  # 永远等待
    finally:
        await runner.cleanup()


# 需要安装 aiohttp: pip install aiohttp
asyncio.run(main())
