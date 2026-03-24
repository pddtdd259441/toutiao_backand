from sqlalchemy import ForeignKey, Index, Integer, UniqueConstraint,DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from models.users import User
from models.news import News
class Base(DeclarativeBase):
    pass
class Favorite(Base):
    # 收藏列表的ORM模型
    __tablename__= "favorite"
    # 在表配置中，创建索引 userid和newsid的
    # 该表中有唯一性约束，使用UniqueConstraint参数来设置 当前新闻，当前用户只能收藏一次
    __table_args__ =( # 表配置要用（）
        UniqueConstraint('user_id','news_id',name='user_news_unqiue'),
        Index('fk_favorite_user_idx','user_id'),
        Index('fk_favorite_news_idx','news_id'),
    )
    # 定义属性 和数据库表保持一致
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="收藏ID")
    # 两个外键 userid和newsid
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey(User.id),nullable=False,comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer,ForeignKey(News.id),nullable=False,comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),nullable=False,comment="收藏时间")
    # 定义魔法函数设置控制台打印格式
    def __repr__(self):
        return f"<Favorite(id={self.id},user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})>"

