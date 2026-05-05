from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    biography = Column(String)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    published_year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    ticket_number = Column(String, unique=True)

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    loan_date = Column(Date)
    return_date = Column(Date, nullable=True)
