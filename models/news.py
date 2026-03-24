from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, Integer, String, ForeignKey, Index, Text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
class Base(DeclarativeBase): # 创建基类，包含复用的一些类型
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        comment="创建时间",
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        comment="更新时间",
        default=func.now(),
        onupdate=func.now(),
    )

class Category(Base): # 分类对象继承基类
    __tablename__ = "news_category" # 一定要对应数据表名
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True,comment="分类ID") # autoincrement = True 允许自增
    name: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,comment="分类名称") # unique 是否唯一，nullable,是否为空
    sort_order: Mapped[int] = mapped_column(Integer,default= 0,nullable = False,comment="排序")
    # 定义这个对象在终端或者控制台中打印这个对象应该长什么样子
    def __repr__(self) : # 对象在控制台上打印的格式参数
        return f"<Category(id = {self.id},name = {self.name},sort_order = {self.sort_order})>"
class News(Base): # 新闻对象
    __tablename__ = "news"
    # 创建索引，提升查询速度，
    __table_args__ = (
        Index('fk_news_category_idx','category_id'), # 高频查询场景
        Index('idx_publish_time','publish_time'), # 按发布时间排序
    )
    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255),nullable=False,comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500),comment="新闻简介")
    content: Mapped[str] = mapped_column(Text,nullable=False,comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255),comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50),comment="作者")
    category_id: Mapped[int] = mapped_column(Integer,ForeignKey('news_category.id'),nullable=False,comment="新闻类别")
    views: Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment="发布时间")
    def __repr__(self):
        return f"<News(id={self.id},title={self.title},views={self.views},publish_time={self.publish_time})>"