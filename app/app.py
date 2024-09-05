from flask import Flask, jsonify, request, make_response
from flask_cors import CORS  # Import CORS
import json
import os

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Path to your JSON file
BOOKS_FILE = "books.json"

# Helper function to load books from the JSON file
def load_books():
    """Load books from a file.

    Returns:
        list: A list of books loaded from the file.
    """
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            return json.load(f)
    return []


# Helper function to save books to the JSON file
def save_books(books):
    """
    Save the given list of books to a file.

    Parameters:
    - books (list): A list of books to be saved.

    Returns:
    - None
    """
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)


# Route to get all books
@app.route("/api/books", methods=["GET"])
def get_books():
    """
    Get the list of books.

    Returns:
        list: A list of books.
    """
    books = load_books()
    return jsonify(books)


# Route to add a new book
@app.route("/api/books", methods=["POST"])
def add_book():
    """
    Add a new book to the library.
    Returns:
        Response: The response object containing the newly added book in JSON format.
    """
    books = load_books()
    new_book = request.json
    new_book["id"] = max([book["id"] for book in books] + [0]) + 1  # Auto-increment ID
    books.append(new_book)
    save_books(books)
    return make_response(jsonify(new_book), 201)


# Route to remove a book
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    """
    Remove a book from the library management system.

    Parameters:
    - book_id (int): The ID of the book to be removed.

    Returns:
    - dict: A JSON response indicating the status of the removal operation.
        - If the book is found and removed successfully, the response will contain the message "Book removed successfully".
        - If the book is not found, the response will contain the message "Book not found".

    Raises:
    - None
    """
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            return jsonify({"message": "Book removed successfully"})
    return jsonify({"message": "Book not found"}), 404

# Route to search for a book by ID
@app.route("/api/books/search", methods=["GET"])
def search_book():
    """
    Search for a book by its ID.

    Returns:
        If the book is found, returns a JSON response containing the matching book.
        If the book is not found, returns a JSON response with a message and a status code 404.
    """
    book_id = request.args.get("id")
    books = load_books()
    matching_books = [book for book in books if book["id"] == int(book_id)]
    if matching_books:
        return jsonify(matching_books)
    else:
        return jsonify({"message": "Book not found"}), 404


@app.route("/api/books/borrow/<int:book_id>", methods=["PUT"])
def borrow_book(book_id):
    """
    Borrow a book by setting its "isBorrowed" attribute to True.

    Parameters:
    - book_id (int): The ID of the book to be borrowed.

    Returns:
    - response (Response): The HTTP response containing the borrowed book information if successful,
                          or an error message if the book is not found.

    """
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        book["isBorrowed"] = True
        save_books(books)
        return make_response(jsonify(book), 200)
    return make_response(jsonify({"error": "Book not found"}), 404)


@app.route("/api/books/return/<int:book_id>", methods=["PUT"])
def return_book(book_id):
    """
    Returns a book by setting its "isBorrowed" status to False.

    Parameters:
    - book_id (int): The ID of the book to be returned.

    Returns:
    - response (Response): The HTTP response containing the book information if found, or an error message if not found.
    """
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        book["isBorrowed"] = False
        save_books(books)
        return make_response(jsonify(book), 200)
    return make_response(jsonify({"error": "Book not found"}), 404)


# Enable CORS for the borrow_book route
CORS(app, resources={r"/api/books/borrow/*": {"origins": "http://localhost:5173"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
