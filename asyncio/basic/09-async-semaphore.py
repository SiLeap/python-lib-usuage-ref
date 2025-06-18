import asyncio
import aiohttp
import time


async def fetch_with_semaphore(semaphore, session, url):
    async with semaphore:  # 限制并发请求数
        print(f"Fetching: {url}")
        async with session.get(url) as response:
            return await response.text()


async def main():
    urls = [f"https://httpbin.org/delay/{i % 3}" for i in range(10)]

    # 限制同时只能有 3 个请求
    semaphore = asyncio.Semaphore(3)

    start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(semaphore, session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    end = time.time()
    print(f"Downloaded {len(urls)} URLs in {end - start:.2f} seconds")


# 需要安装 aiohttp: pip install aiohttp
asyncio.run(main())
