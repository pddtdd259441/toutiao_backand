from fastapi import FastAPI

from routers import favorite, history, news, users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers
app = FastAPI()
# 注册全局异常处理器函数
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许的源 * 为所有，生产环境要指定
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"], # 允许的请求方法
    allow_headers=["*"], #  允许的请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
# 挂载路由，app.include_router()
app.include_router(news.router)# 挂载news路由(注册)
app.include_router(users.router) # 挂载user路由
app.include_router(favorite.router) # 挂载favorite路由
app.include_router(history.router) # 挂载history路由