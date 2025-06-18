import asyncio
import contextvars
import time
"""
使用上下文变量在不同的异步函数间传递信息
无需手动传递参数就能维护请求上下文
构建更复杂的异步应用结构
"""
# 创建上下文变量
request_id = contextvars.ContextVar('request_id', default=None)
user_id = contextvars.ContextVar('user_id', default=None)


# 异步中间件 - 设置上下文
async def context_middleware(next_handler):
    # 为每个请求生成唯一ID
    req_id = f"req-{time.time()}"
    # 设置上下文变量
    request_id.set(req_id)
    user_id.set("user-123")

    print(f"[中间件] 设置请求ID: {req_id}")

    # 调用下一个处理器
    result = await next_handler()

    print(f"[中间件] 完成请求: {req_id}")
    return result


# 异步处理程序
async def handler():
    # 在任何异步函数中都可以访问上下文变量
    print(f"[处理器] 处理请求 {request_id.get()} 用户: {user_id.get()}")

    # 调用其他异步函数
    await asyncio.gather(
        background_task(),
        database_query()
    )

    return {"status": "success", "request_id": request_id.get()}


# 后台任务 - 自动继承上下文
async def background_task():
    # 上下文自动传递
    current_req = request_id.get()
    print(f"[后台任务] 为请求 {current_req} 执行任务")
    await asyncio.sleep(1)


# 数据库查询 - 也会自动继承上下文
async def database_query():
    # 同样可以访问当前请求上下文
    print(f"[数据库] 查询用户数据 - 请求ID: {request_id.get()}, 用户ID: {user_id.get()}")
    await asyncio.sleep(0.5)


# 应用入口
async def application():
    # 包装处理器添加中间件
    return await context_middleware(handler)


# 运行应用
result = asyncio.run(application())
print(f"结果: {result}")
