import asyncio
import functools
import time
from concurrent.futures import ThreadPoolExecutor
"""
1. 允许重用现有同步库
2. 实现渐进式异步改造
3. 在异步代码中使用同步库而不阻塞事件循环
4. 可以同时支持同步和异步API，方便过渡
"""

# 同步API
class SyncDatabase:
    def connect(self):
        print("同步连接数据库")
        time.sleep(1)  # 模拟连接
        return "连接成功"

    def query(self, sql):
        print(f"同步执行查询: {sql}")
        time.sleep(2)  # 模拟查询
        return ["结果1", "结果2", "结果3"]

    def close(self):
        print("同步关闭连接")
        time.sleep(0.5)  # 模拟关闭


# 异步适配器
class AsyncDatabaseAdapter:
    def __init__(self, sync_db, executor=None):
        self.sync_db = sync_db
        self.executor = executor or ThreadPoolExecutor()
        self.loop = None

    async def connect(self):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # 将同步方法包装在线程池中执行
        return await self.loop.run_in_executor(
            self.executor, self.sync_db.connect
        )

    async def query(self, sql):
        # 确保已有事件循环
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # 将同步查询包装为异步
        return await self.loop.run_in_executor(
            self.executor,
            functools.partial(self.sync_db.query, sql)
        )

    async def close(self):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # 将同步关闭包装为异步
        return await self.loop.run_in_executor(
            self.executor, self.sync_db.close
        )


# 异步应用代码
async def main():
    # 创建同步数据库实例
    sync_db = SyncDatabase()

    # 通过适配器将其包装为异步API
    db = AsyncDatabaseAdapter(sync_db)

    # 现在可以使用异步风格操作数据库
    await db.connect()

    # 并发执行多个查询
    results = await asyncio.gather(
        db.query("SELECT * FROM table1"),
        db.query("SELECT * FROM table2"),
        db.query("SELECT * FROM table3")
    )

    for i, result in enumerate(results):
        print(f"查询 {i + 1} 结果: {result}")

    await db.close()


# 运行异步程序
asyncio.run(main())
