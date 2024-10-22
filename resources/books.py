import uuid
from bson import ObjectId
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Schemas.schemas import BookSchema, BookPatchSchema
from db import books_collection, stores_collection
from db import redis_client

blp = Blueprint("books", __name__, description="Operations on books")

@blp.route("/book/<string:bookID>")
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, bookID):
        book = redis_client.get(f"book:{bookID}")
        if book:
            return jsonify(eval(book))
        
        book = books_collection.find_one({"id": bookID})
        if book is None:
            abort(404, message="Book not found")
        
        book["_id"] = str(book["_id"])
        redis_client.setex(f"book:{bookID}", 600, str(book))
        
        return jsonify(book)

    def delete(self, bookID):
        result = books_collection.delete_one({"id": bookID})
        if result.deleted_count == 0:
            abort(404, message="Book not found")
        
        redis_client.delete(f"book:{bookID}")
        
        return {"message": "Book has been deleted"}

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, bookID):
        book = books_collection.find_one({"id": bookID})
        if book is None:
            abort(404, message="Book not found")
        
        books_collection.update_one({"id": bookID}, {"$set": book_data})
        updated_book = books_collection.find_one({"id": bookID})

        redis_client.setex(f"book:{bookID}", 600, str(updated_book))

        return updated_book

    @blp.arguments(BookPatchSchema)
    def patch(self, book_data, bookID):
        book = books_collection.find_one({"id": bookID})
        if book is None:
            abort(404, message="Book ID not found")

        updates = {}
        if "price" in book_data:
            updates["price"] = book_data["price"]
        if "storeID" in book_data:
            updates["storeID"] = book_data["storeID"]
        if "title" in book_data:
            updates["title"] = book_data["title"]
        if "author" in book_data:
            updates["author"] = book_data["author"]
        if "isbn" in book_data:
            updates["isbn"] = book_data["isbn"]

        if updates:
            books_collection.update_one({"id": bookID}, {"$set": updates})
        
        updated_book = books_collection.find_one({"id": bookID})

        redis_client.setex(f"book:{bookID}", 600, str(updated_book))

        return updated_book

@blp.route("/book")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        
        books = list(books_collection.find())
        if not books:
            abort(404, message="No books were found")
        return books
    
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):
        if books_collection.find_one({"title": book_data["title"], "storeID": book_data["storeID"]}):
            abort(400, message="Book already exists")
        
        if not stores_collection.find_one({"id": book_data["storeID"]}):
            abort(404, message="Bookstore not found")

        bookID = uuid.uuid4().hex
        newBook = {**book_data, "id": bookID}
        books_collection.insert_one(newBook)

        redis_client.setex(f"book:{bookID}", 600, str(newBook))

        return newBook, 201

@blp.route("/book/title/<string:title>")
class bookTitles(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self, title):
        
        matching_books = list(books_collection.find({"title": {"$regex": title, "$options": "i"}}))

        if matching_books:  
            for book in matching_books:
                book["_id"] = str(book["_id"])
            return jsonify(matching_books)

        abort(404, message="No books found matching the title")
