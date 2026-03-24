from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
ASYNC_DATABASE_URL = "mysql+aiomysql://root:xxxxxx@localhost:3306/news_app?charset=utf8mb4"
async_engine = create_async_engine( # 创建异步数据引擎
    ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow = 20
)
AsyncSessionLocal = async_sessionmaker( # 创建异步数据工厂
    bind = async_engine,
    expire_on_commit = False,
    class_ = AsyncSession
)
async def get_db(): # 创建异步会话依赖项
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise



