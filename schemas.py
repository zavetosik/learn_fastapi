from pydantic import BaseModel, AnyUrl, Field


class BookCreateSchema(BaseModel):
    title: str = Field(default='Я, легенда')
    image: AnyUrl = Field(default='https://upload.wikimedia.org/wikipedia/uk/1/18/I_Am_Legend_%28ukr_poster%29.jpg')
    price: float = Field(ge=1)
    author: str = Field(default='Річард Метісон')


class BookSavedSchema(BookCreateSchema):
    id: str