import asyncio
import random
import time
"""
任务创建与管理
超时和取消处理
并发控制和错误处理
服务降级策略
复杂异步业务流程编排
"""

# 模拟超时异步操作
async def fetch_data(service_name, timeout=None):
    print(f"开始请求服务: {service_name}")

    # 随机处理时间
    process_time = random.uniform(0.5, 3.0)

    try:
        # 执行有超时限制的操作
        if timeout:
            await asyncio.wait_for(asyncio.sleep(process_time), timeout=timeout)
        else:
            await asyncio.sleep(process_time)

        print(f"服务 {service_name} 返回数据")
        return f"{service_name} 的数据"

    except asyncio.TimeoutError:
        print(f"服务 {service_name} 请求超时")
        return None
    except asyncio.CancelledError:
        print(f"服务 {service_name} 请求被取消")
        # 清理操作
        await asyncio.sleep(0.1)
        print(f"服务 {service_name} 清理完成")
        # 重新抛出异常使任务真正取消
        raise


# 创建具有降级策略的服务请求
async def service_with_fallback(primary, fallback, timeout=1.0):
    # 尝试主服务
    try:
        primary_task = asyncio.create_task(fetch_data(primary, timeout))
        result = await primary_task
        if result:
            return result
    except Exception as e:
        print(f"主服务 {primary} 失败: {e}")

    # 主服务失败，使用备用服务
    print(f"切换到备用服务: {fallback}")
    return await fetch_data(fallback, timeout=2.0)


# 复杂业务流程
async def process_request(request_id):
    print(f"开始处理请求 {request_id}")
    start = time.time()

    # 创建取消时间
    cancel_event = asyncio.Event()

    # 创建看门狗任务
    async def watchdog():
        try:
            # 等待取消事件或5秒后超时
            await asyncio.wait_for(cancel_event.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            # 请求处理时间过长，取消所有任务
            print(f"请求 {request_id} 处理时间过长，取消所有操作")
            for task in tasks:
                if not task.done():
                    task.cancel()

    # 启动看门狗
    watchdog_task = asyncio.create_task(watchdog())

    try:
        # 创建并行任务
        auth_task = asyncio.create_task(
            service_with_fallback("Auth-Primary", "Auth-Backup", timeout=1.5)
        )
        data_task = asyncio.create_task(
            service_with_fallback("Data-Primary", "Data-Backup", timeout=2.0)
        )

        # 同时监控这些任务
        tasks = [auth_task, data_task]

        # 等待所有任务完成或被取消
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果
        auth_result, data_result = results

        # 检查结果类型
        if isinstance(auth_result, Exception):
            print(f"认证服务出错: {auth_result}")
            return {"error": "认证失败"}

        if isinstance(data_result, Exception):
            print(f"数据服务出错: {data_result}")
            return {"error": "数据获取失败"}

        # 正常响应
        response = {
            "request_id": request_id,
            "auth": auth_result,
            "data": data_result,
            "time_ms": (time.time() - start) * 1000
        }
        print(f"请求 {request_id} 处理完成: {response}")
        return response

    except asyncio.CancelledError:
        print(f"请求 {request_id} 被取消")
        # 可以在这里添加清理代码
        raise
    finally:
        # 通知看门狗任务可以结束
        cancel_event.set()
        # 等待看门狗任务完成
        await watchdog_task


# 模拟多个请求
async def main():
    # 并行处理多个请求
    tasks = [
        process_request(f"req-{i}")
        for i in range(3)
    ]

    # 等待所有请求处理完成
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 汇总结果
    success = sum(1 for r in results if not isinstance(r, Exception))
    print(f"处理完成: {success}/{len(tasks)} 请求成功")


# 运行主函数
asyncio.run(main())
