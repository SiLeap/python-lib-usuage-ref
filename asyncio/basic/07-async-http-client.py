import asyncio
import aiohttp
import time


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = [
        "https://python.org",
        "https://gitee.com/"
    ]

    start = time.time()

    async with aiohttp.ClientSession() as session:
        # 并发请求所有 URL
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for url, html in zip(urls, results):
            print(f"{url}: {len(html)} bytes")

    end = time.time()
    print(f"Downloaded {len(urls)} sites in {end - start:.2f} seconds")


# 需要安装 aiohttp: pip install aiohttp
asyncio.run(main())
