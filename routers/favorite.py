from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListRespons, FavoriteNewsItemResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix = "/api/favorite",tags=["favorite"]) # 创建favorite的APIRouter路由实例
# 指定前缀和类别
# 是否收藏
@router.get("/check")
async def check_favorite(news_id: int = Query(...,alias="newsId"),user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    # 参数需要新闻的ID，需要依赖注入验证请求头，需要异步会话
    is_favorite = await favorite.is_news_favorite(db,user.id,news_id)
    # 这里面不能直接返回
    return success_response(message="检查收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorite)) # 这里面data需要构建一个pydantic模型类
# 添加收藏
@router.post("/add")
async def get_favorite(data: FavoriteAddRequest,db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user)):
    # 添加收藏，响应结果
    result = await favorite.add_news_favorite(db,data.news_id,user.id)
    return success_response(message="添加收藏成功",data = result)
 # 取消收藏
@router.delete("/remove")
async def delete_favorite(db: AsyncSession = Depends(get_db),news_id: int = Query(...,alias="newsId"),user: User = Depends(get_current_user)):
    # 验证用户，删除收藏，检查命中，返回响应
    result = await favorite.delete_news_favorite(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="收藏记录不存在")
    return success_response(message="删除收藏成功")

# 获取收藏列表
@router.get("/list")
async def get_favorite_list(page:int = Query(1,ge = 1),pagesize: int = Query(10,le = 100,alias="pageSize"),db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user)):
    #  验证用户， 获取 page,pagesize, 计算收藏你数量，连表查询（包含收藏数据和新闻数据），分页，是否还有更多，返回响应
    #  连表查询 select(主体）.join(另一个表) 
    raws,total = await favorite.get_favorite_list(user.id,db,page,pagesize) # 获取到的ORM对象，需要构建pydantic对象
    # raws 中是一个元组类型， 需要将其转换为dict类型
    favorite_list = [{ # 创建一个新的字典
        **news.__dict__, # __dict__取出这里面的所有属性，**解包这里面的键值对添加到当前的字典当中
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news,favorite_time,favorite_id in raws 
    ] # 这里面是列表推导式， 遍历这里面的每一项，将其转换为字典，最后组合成一个列表
    has_more = total > page*pagesize # 是否还有剩余
    # 导入响应的pydantic对象,并赋值
    data = FavoriteListRespons(
        list = favorite_list,
        total = total,
        hasMore = has_more
    )
    return success_response(message = "获取收藏列表成功",data = data )

# 清空收藏列表
@router.delete("/clear")
async def clear_favorite(db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user)):
    counts = await favorite.remove_all_favorite(db,user.id)
    return success_response(message=f"清空了{counts}条收藏成功")