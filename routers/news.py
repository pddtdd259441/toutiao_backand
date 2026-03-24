# 导入APIRouter
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news, news_cache

#创建APIRouter实例 前缀为/api/news 具体在API文档中
router = APIRouter(prefix="/api/news", tags=["news"])
# 路由
@router.get("/categories") # 获取新闻分类
async def get_categories(skip: int = 0, limit: int = 100,db: AsyncSession = Depends(get_db)): # 依赖注入config中的session
    # 获取数据库里面的新闻分类数据，先定义模型类，封装查询数据的方法，再在这里调用
    categories =  await news_cache.get_categories(db,skip,limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories,
    }
# 获取新闻列表
@router.get("/list")
async def get_news_list(
        category_id: int = Query(...,alias="categoryId"), # Query() alias 多名
        page: int = 1,
        page_size: int = Query(10,alias = "pageSize",le = 100),
        db: AsyncSession = Depends(get_db), # 注入数据库依赖
):
    # 处理分页规则，查询新闻列表，计算总量，计算是否还有更多，
    # 调用查询CURD获取新闻列表
    news_list = await news_cache.get_news_list(db,category_id,page,page_size)
    # 调用统计的CURD操作，获取按类查询的新闻总数
    total = await news_cache.get_news_count(db,category_id)
    # （跳过的+当前列表里面的数量）< 总量
    has_more = (page - 1) * page_size + len(news_list) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        },

    }
# 获取新闻详情
@router.get("/detail")
async def get_news_detail(news_id: int = Query(...,alias="id"),db: AsyncSession = Depends(get_db)):
    # 按照id 查找新闻
    news_detail = await news.get_news_detail(db,news_id)
    if news_detail is None:
        raise HTTPException(status_code=404,detail="新闻不存在")
    # 浏览量增加
    views_res = await news.increase_news_views(db,news_detail.id)
    if not views_res: # 更新view检查是否命中
        raise HTTPException(status_code=404,detail ="新闻不存在")
    # 获取同类新闻
    related_news = await news.get_related_news(db,news_detail.id,news_detail.category_id)

    return {
      "code": 200,
      "message": "success",
      "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
  }
}
# 在main中挂载路由
