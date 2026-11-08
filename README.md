# FastAPI Lab: Book Management API

This project implements a FastAPI server and a Python client to manage a collection of books using RESTful APIs and JSON serialization.

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. Install dependencies: `pip install -r requirements.txt`

## Running the server
```bash
cd server
python main.py
```

## Aditional Exercises/Features
1. Search Books by Genre - This feature provides an endpoint for looking up books by genre. It also supports client-side command parsing.
Endpoint: `/books/genre/{genre}`. For example, `/books/genre/Fiction` would return all fictional books.
Client-side command: `python client.py search-genre "Fiction"` would return all fictional books.

2. Book Ratings - This feature extends the Pydantic Book model by adding a ratings fields. This field stores a list of ratings for a book.

3. Partial Update PATCH - This feature provides an endpoint for partially updating book records. It also supports a client-side command for partial updates.
Enpoint: `/books/{book_id}`
Client-side command: `python client.py patch 1 --title "New Title"` would update the title of book with id 1 to "New Title."

4. Book Count - This feature provides an endpoint for querying the total count of books. It also supports a client-side command for this purpose.
Endpoint: `books/count`. For example, `books/count` would return `{"count": 2}` if there are two books in the database or local memory.
Client-side command: `python client.py count`. This command would return `{"count": 2}` if there are two books in the database or local memory.
