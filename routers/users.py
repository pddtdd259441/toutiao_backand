from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users
from models.users import User
from schemas.user import UserChangePasswordRequest, UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix = "/api/user", tags=["user"]) #user api实例
@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_db)):# 用户数据需要请求体参数做pydantic校验 ，数据库依赖项,需要请求体参数
    # 查询用户信息，判断是否存在，验证用户信息,添加用户
    existing_user = await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户信息已经存在")
    user = await users.create_user(db,user_data)
    # token 创建
    token = await users.create_token(db,user.id)
    # 组装响应
    response_data = UserAuthResponse(token = token,userInfo=UserInfoResponse.model_validate(user))# 按照UserInfoResponse的对象格式，model_validate()方法强制将ORM对象user进行数据校验和过滤，抓取user.id,user.username,...
    # 然后将组装好的UserInfoResponse对象结合token对象封装为UserAuthResponse类型的数据，赋值给response_data,此时已经是一个严格校验的pydantic模型实例
    return success_response(message="注册成功",data=response_data) # 调用响应函数，返回标准的json响应

# 用户登录
@router.post("/login")
async def login(user_data: UserRequest,db: AsyncSession = Depends(get_db)):
    # 查找验证用户是否存在，查找密码解密验证是否一致，生成Token，返回响应
    # 调用验证用户函数
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名密码错误")
    # 生成Token
    token = await users.create_token(db,user.id)
    # 构建返回的data信息
    response_data = UserAuthResponse(token = token,userInfo = UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)
# 查看用户信息
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    # 从请求中获取Token, 查Token和用户，整合这个crud操作，路由调用采用依赖注入的方式注入这个方法
    return success_response(message="获取成功",data=UserInfoResponse.model_validate(user))
    # 这里无法在使用docs验证，无法获取token
# 更改用户信息
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)): # 这里面的db是因为要调用curd中的更新函数
    # 修改用户信息（调用验证用户函,更新用户信息update,响应结果给前端） 参数：请求体参数，使用定义好的请求体参数，依赖注入的验证方法，db
    # 调用更新操作
    user_update = await users.update_user(db,user_data,user.username)
    return success_response(message="更新用户信息成功",data = UserInfoResponse.model_validate(user_update)) # 把 user_update 按照 UserInfoResponse 这个 Pydantic 模型的规则，做校验、类型转换，并最终生成一个 UserInfoResponse 类型的对象。
# 修改用户密码
@router.put("/password")
async def update_password(password_data: UserChangePasswordRequest,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    # 验证用户，获取旧密码，验证新密码，更新密码，返回响应
    # 验证当前密码是否与数据库中的密码一致，调用密码修改函数
    res_change_pwd = await users.change_password(db,password_data.old_password,password_data.new_password,user)
    if not res_change_pwd:
        raise HTTPException(status_code=500,detail="修改密码失败，请稍后再试")
    return success_response(message="密码修改成功")
