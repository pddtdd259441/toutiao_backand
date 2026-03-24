from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase
# favorite响应的pydantic类型
class FavoriteCheckResponse(BaseModel):
    isFavorite: bool = Field(...,alias="isFavorite") # 多名符合驼峰
# 添加收藏需要调用的请求体参数
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")
# 定义新闻模型类，定义收藏模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias = "favoriteId")
    favorite_time: datetime = Field(alias = "favoriteTime")
    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True
    )

# 添加收藏列表接口响应的模型类
class FavoriteListRespons(BaseModel):
    list: list[FavoriteNewsItemResponse] # 调用收藏模型类
    total: int
    has_more: bool = Field(alias = "hasMore")
    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True
    )
