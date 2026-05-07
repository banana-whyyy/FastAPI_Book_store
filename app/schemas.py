# Описание того, как выглядит JSON, который приходит и уходит через API
from pydantic import BaseModel, Field, ConfigDict


# Описание схем автороов
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Author Name")


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int = Field(..., description="Unique author ID")
    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(AuthorBase):
    name: str | None = Field(None, min_length=3, max_length=100, description="Author Name")
    model_config = ConfigDict(from_attributes=True)


# Описание схем книг
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book title")


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int = Field(..., description="Unique book ID")
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BookBase):
    title: str | None = Field(None, min_length=1, max_length=200, description="Book title")
    author_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


# Описание схем пользователей
class UserBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=200, description="User nickname")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int = Field(..., description="Unique user ID")


class UserUpdate(UserBase):
    nickname: str | None = Field(None, min_length=1, max_length=200, description="User nickname")
