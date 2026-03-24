from datetime import datetime
from typing import Optional
from unicodedata import category
from pydantic import BaseModel, ConfigDict, Field
class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None,alias = "publisedTime")
    model_config = ConfigDict(
        from_attributes= True,
        populate_by_name= True
    )
