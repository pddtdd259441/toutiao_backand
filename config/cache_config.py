
from datetime import datetime
from typing import Any
import redis.asyncio as redis
import json
from sqlalchemy import ExceptionContext
# 创建 Redis 的连接对象
# 创建Redis服务器对象 方便修改
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
redis_client = redis.Redis(
    host = REDIS_HOST, # 服务器地址
    port = REDIS_PORT, # 端口号
    db = REDIS_DB, # 数据库编号
    decode_responses= True # 是否将数据解码为字符串
) 

# 二次封装设置缓存和读取缓存的方法
# 存入数据类型不同，分成两个读取方法复杂数据要序列化为字符串， 普通的字符串是另一个读取方法
# 读取字符串，读取列表或字典，设置缓存
async def get_cache(key: str):
    # 基于连接对象，根据指定的键获取值
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败:{e}") # 如果 Redis 连接失败、网络异常、key 格式异常等情况发生，就进入异常处理。
        return None
async def get_json_cache(key:str): # 把 Redis 里存的 JSON 字符串，转回 Python 的字典或列表
    try:
        data =  await redis_client.get(key)
        if data:
            return json.loads(data) # 反序列化 把字符串转化为python对象
        return None
    except Exception as e:
        print(f"获取JSON失败:{e}")
        return None
# 设置缓存
async def set_cache(key:str,value:Any,expire:int = 3600):
    try:
        # 判断输入的类型
        if isinstance(value,(dict,list)): # 如果类型复杂
            # 转字符串
            value = json.dumps(value,ensure_ascii = False) # 序列化 复杂的python对象转化为字符串，中文正常保存
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败:{e}")
        return False


     