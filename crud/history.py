from re import A
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News

# 浏览添加历史记录
async def add_history(db:AsyncSession,news_id: int,user_id: int):
    # 先查询是否有
    query = select(History).where(History.user_id == user_id,History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    if  history is not None:
        history.view_time = func.now()
        await db.commit()
        await db.refresh(history)
        return history
    else:
        new_history = History(user_id = user_id,news_id = news_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        return new_history
    
# 获取历史记录列表
async def get_history_list(user_id: int,db: AsyncSession,page: int = 1,page_size: int = 10):
    # 查询并统计历史记录数量
    stmt = select(func.count()).where(History.user_id == user_id)
    result = await db.execute(stmt)
    total = result.scalar_one()
    # 连表查询新闻和历史记录，并分页
    query = select(News,History.view_time.label("view_time"),History.id.label("history_id")).join(History,History.news_id == News.id).where(History.user_id == user_id).order_by(History.view_time.desc()).offset((page-1)*page_size).limit(page_size)
    history_result = await db.execute(query)
    history_raws = history_result.all()
    return total,history_raws

# 删除单个历史记录
async def delete_history(db: AsyncSession,user_id: int ,news_id: int):
    stmt = delete(History).where(History.user_id == user_id,History.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# 清空历史列表
async def delete_history_list(db: AsyncSession,user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0