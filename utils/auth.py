# 整合从Header中获取Token 根据Token查询用户，返回用户
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import users


async def get_current_user(authorization: str = Header(...,alias="Authorization"),db: AsyncSession = Depends(get_db),):
    # Bearer 一般请求头都在 Authorization Bearer TOKEN 中 这是必填项，入过没有请求头就无法获取token 
    # token = authorization.split(" ")[1] 按照空格隔开获取第一项
    token = authorization.replace("Bearer ","") # 获取请求头中的Token的两种方法 将Bearer换成""剩下的就是Token
    # 根据Token 调用Token查用户的Curd函数
    user = await users.get_user_by_token(db,token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效的令牌或者是已经过期的令牌")
    return user