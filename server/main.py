from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Define complex object models
class Author(BaseModel):
    name: str
    email: Optional[str] = None

class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    ratings: List[int] = None

class AuthorPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class BookPatch(BaseModel):
    title: Optional[str] = None
    author: Optional[AuthorPatch] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    ratings: Optional[List[int]] = None

# In-memory dataset
books = [
    Book(
            id=1,
            title="The Great Gatsby",
            author=Author(name="F. Scott Fitzgerald", email="fscott@example.com"),
            year=1925,
            genre="Fiction"
        ),
    Book(
        id=2,
        title="1984",
        author=Author(name="George Orwell", email="gorwell@example.com"),
        year=1949,
        genre="Dystopian"
    )
]

# GET all books
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

# Book count
@app.get("/books/count")
async def book_count():
    return {"count": len(books)}

# GET a book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# POST a new book
@app.post("/books", response_model=Book)
async def create_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book)
    return book

# PUT to update a book
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}

    raise HTTPException(status_code=404, detail="Book not found")

# Search book by genre
@app.get("/books/genre/{genre}", response_model=List[Book])
async def get_book_by_genre(genre:str):
    matching_books = [book for book in books if book.genre.casefold() == genre.casefold()]
    if not matching_books:
        raise HTTPException(status_code=404, detail="Book not found")

    return matching_books

# PATCH to partially update a book
@app.patch("/books/{book_id}", response_model=Book)
async def patch_book(book_id: int, updates: BookPatch):
    for book in books:
        if book.id == book_id:
            update_data = updates.model_dump(exclude_unset=True, exclude_none=True)
            author_updates = update_data.pop("author", None)

            for field, value in update_data.items():
                setattr(book,field,value)

            if author_updates:
                for field, value in author_updates.items():
                    setattr(book.author, field, value)

            return book
            
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)