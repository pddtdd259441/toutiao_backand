# 这是抽取统一响应格式的函数
# 成功响应函数
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
def success_response(message: str = "success",data = None):# 需要两个参数，一个是成功信息，另一个是数据对象，这里对象不确定，传进来是啥就是啥
    # 任何使用到的对象都要正常响应 code message data 使用jsonable_encoder进行转化
    content={
        "code":200,
        "message":message,
        "data":data
    }
    # 指定响应的转化格式
    return JSONResponse(content = jsonable_encoder(content))

# 下一步 要定义 不同验证类型的响应格式 要用到请求体参数

