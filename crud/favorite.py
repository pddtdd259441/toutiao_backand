from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import favorite
from models.favorite import Favorite
from models.news import News

# 获取是否收藏信息 ，返回bool值，表示当前新闻是否被收藏
async def is_news_favorite(db: AsyncSession,user_id:int,news_id:int):
    stmt = select(Favorite).where(Favorite.user_id==user_id , Favorite.news_id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None
# 添加收藏
async def add_news_favorite(db: AsyncSession,news_id:int,user_id:int):
    favorite = Favorite(news_id = news_id,user_id = user_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite
# 删除收藏
async def delete_news_favorite(db:AsyncSession,user_id: int,news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# 获取收藏列表 
async def get_favorite_list(user_id: int,db: AsyncSession,page: int = 1,pagesize: int = 10):
    # 某个用户的收藏 获取总量，收藏列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()
    # 连表查询获取收藏列表，按照收藏时间排序，并分页 limit() + offset() 
    query = select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite.id")).join(Favorite,Favorite.news_id == News.id).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc()).offset((page-1)*pagesize).limit(pagesize) # seLect里面是查询主题类,join是联合查询类 里面要有联合查询条件 
    # select()中可以起别名 Favorite.create_at.label("favorite_time")
    # .order_by(Favorite.create_at.desc()) 按时间顺序降序排序
    # 获取到的数据为列表对象 内部有新闻，收藏时间，收藏id
    result = await db.execute(query)
    rows = result.all() # scalars() 只适合一个模型，每一行的第一列，而不适合多个模型，这里查到的是元组，有多个列，所以直接用all
    return rows,total

# 清空收藏列表 
async def remove_all_favorite(db: AsyncSession, user_id: int):
    # 清空当前用户的列表
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0