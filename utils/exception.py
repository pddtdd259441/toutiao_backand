# 开发模式： 返回详细的错误信息
# 生产模式； 返回简化的错误信息
import traceback
from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status
DEBUG_MODE = True # 教学项目保持开启
# 处理HTTPException
async def http_exception_handler(request: Request,exc:HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data":None
        },
        headers = exc.headers
    )
# 处理数据库完整性约束错误 IntegrityError 在数据库错误已经发生后有统一返回一个HTTP JSON响应
async def integrity_error_handler(request: Request,exc: IntegrityError):
    # 获取原始错误信息
    error_msg = str(exc.orig) # 将错误信息转换为字符串
    # 用户已存在
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    # 外键约束失效
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    # 其他错误
    else:
        detail = "数据约束冲突，请检查输入"
    # 开发模式下返回错误详细信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }
        # JSONResponse 打包返回一个JSON响应
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )
# SQLAIchemyError 处理总基类异常 兜底其他
async def sqlalchemy_error_handler(request: Request,exc: SQLAlchemyError):
    # 处理其他SQLAlchemy数据库错误
    # 在开发者模式下查看详细异常信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            # 获取异常类型 SQLAlchemyError type(exc)__name__ 获取对应的类型
            "error_type": type(exc).__name__,
            "error_detail": str(exc), # 获取异常详细信息,这里无需查看底层
            "traceback": traceback.format_exc(), # 获取异常的堆栈跟踪信息
            "path": str(request.url) # 获取异常的路径
        }
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "code": 500,
            "message": "数据库操作失败，请稍后尝试",
            "data": error_data
        }
    )
# 处理其他未捕获的异常通用函数
async def general_exception_handler(request: Request,exc: Exception):
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "code": 500,
            "message": "服务器内部错误，请稍后尝试",
            "data": error_data
        }
    )
        
            

        


    

