from passlib.context import CryptContext
# 创建加密上下文对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 密码加密
def get_hash_password(password: str):
    return pwd_context.hash(password)
# 密码解密 bool型返回 判断两者是否一致
def verify_password(password: str,hashed_password: str):
    return pwd_context.verify(password,hashed_password)