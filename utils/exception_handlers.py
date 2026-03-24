from sqlite3 import IntegrityError
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from utils.exception import general_exception_handler, http_exception_handler, integrity_error_handler, sqlalchemy_error_handler

# 注册全局异常处理器函数
def register_exception_handlers(app: FastAPI): 
    # 子类在前，父类在后，具体在前，抽象在后
    # 挂载业务异常处理函数
    app.add_exception_handler(HTTPException, http_exception_handler)
    # 挂载数据完整性异常处理函数
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    # 挂载数据库SQLAlchemy异常处理函数
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    # 挂载其他异常处理函数（兜底）
    app.add_exception_handler(Exception, general_exception_handler)
