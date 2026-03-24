# 存放新闻相关的缓存方法
# 新闻分类的读取和写入
# key - value 
from typing import Any, Dict, List, Optional
from config.cache_config import get_json_cache, set_cache

# 定义一个常量，新闻分类在Redis缓存键名固定叫：news:categories
CATEGORIES_KEY = "news:categories"
# 获取新闻分类的缓存方法 去 Redis 里读取 news:categories 对应的缓存，并把 JSON 字符串转回 Python 对象
async def get_cache_categories():
    result = await get_json_cache(CATEGORIES_KEY) # 调用读取函数，这里是用的复杂类型的函数
    return result

# 写入新闻分类缓存 数据 和 时间
# 过期时间 分类 配置 7200，列表： 600 详情： 1800 验证码： 120 数据越稳定，缓存越持久 避免所有的key同时过期，缓存雪崩
# 把新闻分类列表写入 Redis，并设置过期时间，默认 7200 秒
async def set_cache_categories(data: list[Dict[str,Any]],expire: int = 7200): # 传入的是一个列表，每一项都是一个字典，字典的第一个值为str,第二个值为任意类型
    return await set_cache(CATEGORIES_KEY,data,expire) # 调用写入的函数

# 定义新闻列表读取写入的方法
# 定义新闻列表key news_list:分类id,页码，每页数量
NEWS_LIST_PREFIX = "news_list"

# 写入缓存 
# 分类列表，分类id,页码，每页数量，列表数据，过期时间
async def set_cache_news_list(category_id: Optional[int],page:int,size:int,news_list:List[Dict[str,Any]],expire: int = 600):
    # 分类id没有的情况，不存在"为all"
    category_part =category_id  if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{size}"
    # 调用 存入方法
    return await set_cache(key,news_list,expire)
# 读取缓存
async def get_cache_news_list(category_id: Optional[int],page:int,size:int):
    category_part =category_id  if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    # 调用读取方法
    return await get_json_cache(key)