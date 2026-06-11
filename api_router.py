from fastapi import APIRouter, status
from schemas import BookCreateSchema, BookSavedSchema
from bson import ObjectId


api_router = APIRouter(
    prefix='/api/books'
)


@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    saved_book = BookSavedSchema(
        title=book.title,
        image=book.image,
        price=book.price,
        author=book.author,
        id=str(ObjectId())
    )
    return saved_book