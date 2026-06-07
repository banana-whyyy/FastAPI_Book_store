# Вся бизнес логика, пользователь не может удалять и обновлять книги
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func, select

from app.models import Book, Author, User
from app.schemas import BookCreate, AuthorCreate, UserCreate, BookUpdate
from app.security import get_password_hash


async def get_author(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(
        select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
    )
    return result.scalar_one_or_none()


async def get_author_by_name(db: AsyncSession, name: str) -> Author | None:
    result = await db.execute(
        select(Author).options(selectinload(Author.books)).where(Author.name == name)
    )
    return result.scalar_one_or_none()


async def get_authors(db: AsyncSession, skip=0, limit=300) -> list[Author]:
    result = await db.execute(select(Author).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_author(db:AsyncSession, author: AuthorCreate) -> Author:
    db_author = Author(**author.model_dump())
    db.add(db_author)
    await db.flush()
    await db.refresh(db_author)
    return db_author


async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(
        select(Book).options(selectinload(Book)).where(Book.id == book_id)
    )
    return result


async def get_book