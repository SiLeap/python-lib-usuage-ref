import asyncio

"""
1. 每个调用异步函数的函数本身也必须是异步的
2. 异步性质会向上传播到整个调用链
3. 修改一个函数为异步可能导致大量代码更改
"""

# 最底层的异步函数
async def fetch_data():
    print("获取数据中...")
    await asyncio.sleep(1)  # 模拟网络请求
    return {"id": 1, "name": "示例数据"}

# 中间层异步函数 - 必须也是异步的
async def process_data():
    data = await fetch_data()  # 调用异步函数必须使用await
    print(f"处理数据: {data}")
    await asyncio.sleep(0.5)  # 模拟处理
    data['processed'] = True
    return data

# 高层异步函数 - 同样必须是异步的
async def save_result():
    processed_data = await process_data()  # 继续传播异步性质
    print(f"保存结果: {processed_data}")
    await asyncio.sleep(0.5)  # 模拟保存
    return "保存成功"

# 应用入口 - 也需要是异步的或使用特殊方法运行异步代码
async def main():
    result = await save_result()
    print(f"最终结果: {result}")

# 运行异步程序
asyncio.run(main())
