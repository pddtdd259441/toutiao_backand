
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryGetListResponse
from utils.auth import get_current_user
from utils.response import success_response

# 创建history的API实例
router = APIRouter(prefix="/api/history",tags=["history"])
# 添加浏览记录
@router.post("/add")
async def add_history(data: HistoryAddRequest,db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user)):
    # post方法，需要引入pydantic请求体参数 
    # 验证用户，添加历史记录(首先要判断该条新闻是否在该用户的浏览记录表里，若有，更新时间，若无，则添加该历史记录)
    added_history = await history.add_history(db,data.news_id,user.id) # 这里一定要加await
    return success_response(message="添加成功",data = added_history)
# 获取浏览记录列表
@router.get("/list")
async def get_history_list(db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user),page: int = 1,page_size: int = Query(10,alias="pageSize",le = 100)):
    # 验证用户， 查询历史记录数量，连表查询新闻和记录信息，分页，判断是否还有剩余，返回响应,响应需要定义pydantic对象
    total,history_raws = await history.get_history_list(user.id,db,page,page_size) # 获取到ORM对象
    history_list = [{
        **news.__dict__,
        "view_time": view_time
    } for news,view_time,history_id in history_raws
    ]
    has_more = total > page*page_size
    data = HistoryGetListResponse(
        list = history_list,
        total = total,
        has_more =  has_more
    )
    return success_response(message="success",data = data)
# 删除历史记录
@router.delete("/delete/{news_id}")
async def delete_history(news_id: int,db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user) ):
    # 验证用户，删除，返回响应
    result = await history.delete_history(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="历史记录不存在")
    return success_response(message="删除成功")

# 清空历史列表
@router.delete("/clear")
async def delete_history_list(db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user)):
    result = await history.delete_history_list(db,user.id)
    return success_response(message = f"删除了{result}条记录")
