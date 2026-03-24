# 用户数据库操作
from configparser import NoOptionError
from pickle import TRUE
import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils import security
from models.users import User, UserToken
from schemas.user import UserRequest, UserUpdateRequest


# 根据用户名查询用户数据
async def get_user_by_username(db: AsyncSession,username: str):
    stmt = select(User).where(User.username == username) # 根据用户名查找用户
    result = await db.execute(stmt)
    return result.scalar_one_or_none() # 返回用户对象
# 添加用户数据
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密处理
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库中读回最新的数据
    return user
# token的创建
async def create_token(db: AsyncSession, user_id: int): # 查找该用户是否有token, 有token更新，没有token创建
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result= await db.execute(stmt)
    # 生成Token uuid，过期时间
    token = str(uuid.uuid4())
    expires_at = datetime.now()+timedelta(days=7) # 返回时间长度
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
    await db.commit()

    return token
# 验证用户函数,是否存在，密码是否一致
async def authenticate_user(db: AsyncSession,username: str,password: str):
    # 调用按照用户名查找用户的函数
    user = await get_user_by_username(db,username)
    # 判断用户是否存在
    if user is None:
        return None
    # 判断密码是否一致，调用解密函数
    if not security.verify_password(password,user.password):
        return None
    # 都没问题，返回user
    return user
# 根据Token查询用户（验证Token是否有效，查找用户）
async def get_user_by_token(db: AsyncSession,token: str):
    # 查询token
    stmt =  select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    # 如果token不存在或者已经过期，返回None
    if db_token is None or db_token.expires_at < datetime.now():
        return None
    # 根据Token类型的外键user_id查找用户
    query = select(User).where(User.id == db_token.user_id)
    result1 = await db.execute(query)
    user = result1.scalar_one_or_none()
    return user
    
# 更新用户信息 update获取更新后的用户返回
async def update_user(db:AsyncSession,user_data: UserUpdateRequest,username:str):
    # values()中需要字段=值的类型 user_data是一个pydantic类型 需要先转换为python字典，解包转换为键值对的格式
    # 没有设置值的不更新,model_dump()中的exclude_unset=True 可以设置不修改的值不导出，exclude_none=True 值为None的不导出
    stmt = update(User).where(User.username==username).values(**user_data.model_dump(exclude_unset=True,exclude_none=True)) # values 
    result = await db.execute(stmt)
    await db.commit()
    # 检查是否更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户不存在")
    # 获取一下更新后的用户信息
    update_user = await get_user_by_username(db,username)
    return update_user
    

# 验证密码及加密修改密码
async def change_password(db: AsyncSession,old_password:str,new_password: str,user: User):
    if not security.verify_password(old_password,user.password): #验证旧密码 如果验证失败，返回False
        return False
    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd
    db.add(user) # 把user对象放到session中，交给ORM管理，确保user始终被session管理
    # 规避 session 过期或者关闭导致的不能提交的问题
    await db.commit()
    await db.refresh(user)
    return True