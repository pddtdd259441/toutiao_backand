from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str

# 响应格式转化类型定义
# user_info对应的类 基础类 包含基础信息（可选的） + Info类（id,用户名）
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None,max_length=50,description="昵称")
    avatar: Optional[str] = Field(None,max_length=255,description="头像")
    gender: Optional[str] = Field(None,max_length=10,description="性别")
    bio: Optional[str] = Field(None,max_length=500,description="个人简介")
class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
            populate_by_name=True,  # 允许使用别名 字段名兼容
            from_attributes=True  # 允许从ORM对象中取值
        )
# 用户信息中组合Token，允许从ORM中提取值，和别名使用
class UserAuthResponse(BaseModel):
    token: str
    userInfo: UserInfoResponse = Field(...,alias="userInfo")
    model_config = ConfigDict(
            populate_by_name=True, # 允许使用别名 字段名兼容
            from_attributes=True # 允许从ORM对象中取值
        )

# 定义更新用户信息用到的请求体参数的类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avator: str = None
    gender: str = None
    bio: str = None
    phone: str = None

# 定义修改密码用到的请求体参数
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(...,description="当前密码",alias="oldPassword")
    new_password: str = Field(...,min_length=6,alias="newPassword",description="新密码")
