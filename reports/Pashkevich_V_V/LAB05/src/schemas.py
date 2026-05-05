from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    published_year: int
    author_id: int
    genre_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    class Config:
        from_attributes = True
