from datetime import datetime
from enum import unique
from typing import Optional

from sqlalchemy import Index, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column

# 基类
class Base(DeclarativeBase):
    pass
# 用户模型类
class User(Base):
    __tablename__ = "user" # 用户表名
    __table_args__ = ( # 创建索引 手机号用户名查询是高频操作
        Index('username_UNIQUE','username'),
        Index('phone_UNIQUE','phone'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,comment="用户ID")
    username: Mapped[str] = mapped_column(String(50),unique=True, nullable=False , comment="用户名")
    password: Mapped[str] = mapped_column(String(50),nullable=False,comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(255),comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255),comment="头像URL",default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male','female','unknown'),comment="性别",default="unknown") # Enum 枚举类型，除了括号内的值意外的其他值都报错
    bio: Mapped[Optional[str]] = mapped_column(String(500),comment="个人简介",default="这个人很懒什么也没有留下")
    phone: Mapped[Optional[str]] = mapped_column(String(20),unique=True,comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),
                                                 comment="更新时间")
    # 控制台打印对象放法
    def __repr__(self):
        return f"<User id = {self.id},username = {self.username},nickname = {self.nickname}.>"
# 用户Token类
class UserToken(Base):
    __tablename__ = "user_token"
    # 创建索引
    __table_args__ = (
        Index('token_UNIQUE','token'),
        Index('fk_user_token_user_idx','user_id'),
    )
    # 属性
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="；令牌ID")
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey(User.id),nullable=False,comment="用户ID")
    token: Mapped[str] = mapped_column(String(255),unique=True,nullable=False,comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False,comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    # 控制台输出的方法
    def __repr__(self):
        return f"<UserToken(id = {self.id},token = {self.token},expires_at = {self.expires_at})>"


