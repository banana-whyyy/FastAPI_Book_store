from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Сравнивает введеный пароль с хэшем из БД
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Хэширует пароль пользователя перед сохранением в БД
def get_password_hash(password) -> str:
    return pwd_context.hash(password)


# Функция создания JWT-токена
def create_access_token(data: dict):
    to_encode = data.copy
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes) 
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)



def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None