import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

def get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    print_response(response)

def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print_response(response)

def create_book(title, author_name, author_email, year, genre, ratings):
    book = {
        "id": len(requests.get(f"{BASE_URL}/books").json()) + 1,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "ratings": ratings
    }
    response = requests.post(f"{BASE_URL}/books", json=book)
    print_response(response)

def update_book(book_id, title, author_name, author_email, year, genre, ratings):
    book = {
        "id": book_id,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "ratings": ratings
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=book)
    print_response(response)

def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    print_response(response)

def get_book_by_genre(genre):
    response = requests.get(f"{BASE_URL}/books/genre/{genre}")
    print_response(response)

def get_book_count():
    response = requests.get(f"{BASE_URL}/books/count")
    print_response(response)

def patch_book(book_id, title=None, author_name=None, author_email=None, year=None, genre=None, ratings=None):
    updates = {}
    if title is not None:
        updates["title"] = title
    if year is not None:
        updates["year"] = year
    if genre is not None:
        updates["genre"] = genre
    if ratings is not None:
        updates["ratings"] = ratings

    author = {}
    if author_name is not None:
        author["name"] = author_name
    if author_email is not None:
        author["email"] = author_email
    if author:
        updates["author"] = author

    response = requests.patch(f"{BASE_URL}/books/{book_id}", json=updates)
    print_response(response)

def print_response(response):
    try:
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(f"Status Code: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Book API Client")
    subparsers = parser.add_subparsers(dest="command", help="API command")

    # List all books
    subparsers.add_parser("list", help="List all books")

    # Get a book
    get_parser = subparsers.add_parser("get", help="Get a book by ID")
    get_parser.add_argument("id", type=int, help="Book ID")

    # Create a book
    create_parser = subparsers.add_parser("create", help="Create a new book")
    create_parser.add_argument("title", type=str, help="Book title")
    create_parser.add_argument("author_name", type=str, help="Author name")
    create_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    create_parser.add_argument("year", type=int, help="Publication year")
    create_parser.add_argument("genre", type=str, help="Book genre")
    create_parser.add_argument("ratings", type=int, nargs="+", help="Book ratings")

    # Update a book
    update_parser = subparsers.add_parser("update", help="Update a book")
    update_parser.add_argument("id", type=int, help="Book ID")
    update_parser.add_argument("title", type=str, help="Book title")
    update_parser.add_argument("author_name", type=str, help="Author name")
    update_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    update_parser.add_argument("year", type=int, help="Publication year")
    update_parser.add_argument("genre", type=str, help="Book genre")
    update_parser.add_argument("ratings", type=int, nargs="+", help="Book ratings")

    # Partially udpate a book
    patch_parser = subparsers.add_parser("patch", help="Partially update a book")
    patch_parser.add_argument("id", type=int, help="Book ID")
    patch_parser.add_argument("--title", type=str, help="Book title")
    patch_parser.add_argument("--author-name", type=str, help="Author name")
    patch_parser.add_argument("--author-email", type=str, help="Author email")
    patch_parser.add_argument("--year", type=int, help="Publication year")
    patch_parser.add_argument("--genre", type=str, help="Book genre")
    patch_parser.add_argument("--ratings", type=int, nargs="+", help="Book ratings")

    # Delete a book
    delete_parser = subparsers.add_parser("delete", help="Delete a book")
    delete_parser.add_argument("id", type=int, help="Book ID")

    # Search books by genre
    search_parser = subparsers.add_parser("search-genre", help="Search books by genre")
    search_parser.add_argument("genre", type=str, help="Book genre")

    # Get book count
    subparsers.add_parser("count", help="Get book count")
    

    args = parser.parse_args()

    if args.command == "list":
        get_all_books()
    elif args.command == "get":
        get_book(args.id)
    elif args.command == "create":
        create_book(args.title, args.author_name, args.author_email, args.year, args.genre, args.ratings)
    elif args.command == "update":
        update_book(args.id, args.title, args.author_name, args.author_email, args.year, args.genre, args.ratings)
    elif args.command == "delete":
        delete_book(args.id)
    elif args.command == "search-genre":
        get_book_by_genre(args.genre)
    elif args.command == "count":
        get_book_count()
    elif args.command == "patch":
        patch_book(args.id, args.title, args.author_name, args.author_email, args.year, args.genre, args.ratings)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()