# Описание того, как выглядит JSON, который приходит и уходит через API
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr

from app.models import UserRole


# Описание схем автороов
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Author Name")
    bio: str | None = None
    birth_date: date

    @field_validator("birth_date")
    @classmethod
    def not_in_future(cls, d: date) -> date:
        if d > date.today():
            raise ValueError("birth date cannot be in future")
        return d




class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



# Описание схем книг
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    description: str
    price: int = Field(..., ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    author_id: int


class BookCreate(BookBase):
    pass


class BookResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    price: int
    stock_quantity: int
    author_id: int
    author: AuthorResponse
    created_at: datetime


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, description="Book title")
    description: str | None = None
    price: int | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)


class BookListResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    price: int
    stock_quantity: int
    author_id: int
    created_at: datetime


class AuthorWithBookResponse(AuthorResponse):
    books: list[BookListResponse] = []


# Описание схем пользователей
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: int 
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    role: UserRole


# Описание схем токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Описание схем заказа
class OrderCreate(BaseModel):
    book_id: int
    quantity: int = Field(..., gt=0)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    quantity: int
    total_price: int
    created_at: datetime


class PaginatedBooks(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int
