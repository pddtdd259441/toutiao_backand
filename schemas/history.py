from dataclasses import field
from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase
# 添加历史浏览用到的请求体参数
class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId",description="新闻id")

# 获取历史查询列表的请求体参数
class HistoryGetList(NewsItemBase):
    view_time: datetime = Field(...,alias="viewTime")
    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True
    )
# 获取历史查询列表的响应参数
class HistoryGetListResponse(BaseModel):
    list: list[HistoryGetList]
    total: int 
    has_more: bool = Field(...,alias="hasMore")
    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True
    )
