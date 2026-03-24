# 改造后带有缓存的news curd 操作
import json
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from cache.news_cache import get_cache_categories, get_cache_news_list, set_cache_categories, set_cache_news_list
from models.news import Category, News
from fastapi.encoders import jsonable_encoder

from schemas.base import NewsItemBase
# 查询新闻类
async def get_categories(db:AsyncSession,skip: int = 0 ,limit: int = 100):# 默认要放到非默认后面
    # 获取新闻分类 先查询缓存
    news_cat = await get_cache_categories()
    if news_cat: # 如果有数据
        return news_cat  # 返回
    # 如果没有 查库
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categpories = result.scalars().all()
    # 写入缓存
    if categpories: 
        # result 是ORM数据， 需要进行转化 
        categpories = jsonable_encoder(categpories) # 可以把ORM对象转化为可以转换为json的对象
        await set_cache_categories(categpories)
    # 返回数据
    return categpories
# 查询新闻列表
async def get_news_list(db:AsyncSession,category_id: int,page: int = 0,limit: int = 10):
    # 先查询缓存
    news_list_cache = await get_cache_news_list(category_id,page,limit) 
    if news_list_cache: # 从缓存中取出的是字典列表，想返回ORM对象，需要将字典重构
        return [News(**item) for item in news_list_cache] # 从缓存中查询的字典解包转换为News对象
    # 未命中 先查询数据库
    stmt =  select(News).where(News.category_id == category_id).offset((page-1)*limit).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()
    # 写入缓存
    if news_list: # 如果没有命中
        # 把ORM对象的数据转换字典写入缓存 先ORM转换成pydantic类型
        news_data = [NewsItemBase.model_validate(item).model_dump(mode = "json", by_alias=False) for item in news_list]
        # 先把ORM对象item验证，并转换为NewsItemBase这个Pydantic模型（可以直接从pydantic对象中提取值）
        # model_dump 将pydantic对象转换为字典，mode = json 表示按照json的格式导出，导出时用字段的原名
        await set_cache_news_list(category_id,page,limit,news_data)
    return news_list
# 计算查询新闻的总量
async def get_news_count(db:AsyncSession,category_id: int): # 查询指定类的总数
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() # 提取聚合计算的统计结果,scalar_one()只能有一个否则报错
# 查找当前新闻
async def get_news_detail(db:AsyncSession,news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
# 增加浏览量
async def increase_news_views(db:AsyncSession,news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    # 更新并立刻提交数据库
    result = await db.execute(stmt)
    await db.commit()
    # 数据库更新操作，要检查数据库是否真的命中数据
    # 命中返回True,False 反之
    return result.rowcount > 0
# 获取同类新闻
async def get_related_news(db:AsyncSession,news_id: int,category_id: int,limit: int =5):
    stmt = select(News).where(News.id != news_id,News.category_id == category_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit) # order_by按照某种排序获取,默认是升序，desc表示降序
    result = await db.execute(stmt)
    # return result.scalars().all()
    # 按照指定结果类型返回 使用列表推导式，推导出核心数据 然后return
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "categoryId": news.category_id,
        "views": news.views,
    }for news in result.scalars().all()]

