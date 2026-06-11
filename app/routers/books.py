from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_book, get_book, get_book_for_update, get_books, update_book, get_author, delete_book
from app.models import User
from app.schemas import BookCreate, BookResponse, PaginatedBooks, BookUpdate
from app.database import get_db
from app.dependencies import get_admin_user

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=PaginatedBooks)
async def list_books(offset: int=0, limit: int=20, author_id: int | None = None, db: AsyncSession =Depends(get_db)):
    books, total = await get_books(db, skip=offset, limit=limit, author_id=author_id)
    return PaginatedBooks(items=books, total=total, limit=limit, offset=offset)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book_detail(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    _:User = Depends(get_admin_user),
    ):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    
    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
    _:User = Depends(get_admin_user),
):
    author = await get_author(db, book.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author not found",
        )

    return await create_book(db, book)


@router.patch("/{book_id}", response_model=BookResponse)
async def modify_book(
    book_id: int, 
    book_update: BookUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    update = await modify_book(db, book_id, book_update)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    
    return update



@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    deleted = await delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    
    await db.commit()  
    return None