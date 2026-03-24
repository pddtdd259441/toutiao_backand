# toutiao_backand
黑马的FastAPI 课程的项目
一个基于 FastAPI 的新闻后端项目，提供新闻浏览、用户注册登录、收藏与历史记录等接口。前端在黑马公众号中获取链接

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x（异步）
- MySQL（`aiomysql` 驱动）
- Passlib（`bcrypt`）密码加密
- Uvicorn

## 项目功能

- 用户模块
  - 用户注册
  - 用户登录
  - 获取用户信息
  - 更新用户信息
  - 修改密码
- 新闻模块
  - 获取新闻分类
  - 按分类分页获取新闻列表
  - 获取新闻详情
  - 增加浏览量
- 收藏模块
  - 检查是否收藏
  - 添加收藏
  - 取消收藏
  - 获取收藏列表
  - 清空收藏
- 历史记录模块
  - 添加浏览记录
  - 获取浏览记录列表
  - 删除单条记录
  - 清空历史记录

## 项目结构

```text
toutiao_backand/
├─ main.py                  # 应用入口，注册中间件和路由
├─ config/
│  └─ db_config.py          # 数据库连接与会话
├─ routers/                 # 路由层
├─ crud/                    # 数据访问层
├─ models/                  # SQLAlchemy 模型
├─ schemas/                 # Pydantic 请求/响应模型
├─ utils/                   # 工具函数（鉴权、响应封装、异常处理）
└─ test_main.http           # 简单接口测试文件
```

## 快速开始

### 1) 克隆并进入项目

```bash
git clone <your-repo-url>
cd toutiao_backand
```

### 2) 创建并激活虚拟环境

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) 安装依赖

当前仓库未包含 `requirements.txt`，可先安装项目已使用到的核心依赖：

```bash
pip install fastapi uvicorn sqlalchemy aiomysql passlib bcrypt pydantic
```

### 4) 配置数据库

数据库连接配置位于 `config/db_config.py`：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://root:xxxxxx@localhost:3306/news_app?charset=utf8mb4"
```

请按你的本地环境修改用户名、密码、主机、端口与数据库名，并确保 MySQL 中已创建对应数据表。

### 5) 启动服务

```bash
uvicorn main:app --reload
```

服务默认启动在 `http://127.0.0.1:8000`。

## 接口文档

启动后可访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 接口前缀

- 用户：`/api/user`
- 新闻：`/api/news`
- 收藏：`/api/favorite`
- 历史：`/api/history`

## 鉴权说明

部分接口需要携带登录后的 token，请在请求头中添加：

```http
Authorization: Bearer <token>
```

项目通过 `utils/auth.py` 从请求头解析 token，并在数据库中校验有效期。

## 测试

可使用 `test_main.http` 做基础连通性测试，或通过 Swagger 页面直接调试接口。

## 注意事项

- 当前数据库连接信息写在代码中，仅适合本地开发，建议改为环境变量配置。
- 仓库中存在 `__pycache__` 等编译产物，建议加入 `.gitignore` 统一忽略。
- 生产环境请收紧 CORS 配置，不建议使用 `allow_origins=["*"]`。
