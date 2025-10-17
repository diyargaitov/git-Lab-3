from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Библиотеки Книг")

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int

books: List[Book] = [
    Book(id=1, title="1984", author="Джордж Оруэлл", year=1949),
    Book(id=2, title="Мастер и Маргарита", author="М. Булгаков", year=1967),
]

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books", response_model=Book)
def add_book(book: Book):
    book.id = len(books) + 1
    books.append(book)
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            updated.id = book_id
            books[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Книга удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")
