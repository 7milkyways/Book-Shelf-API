from flask import jsonify, request, abort
from flask_migrate import Migrate
from flask_cors import CORS
from models import *

CORS(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/bookdb'

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')

    return response

@app.route('/books', methods=['GET'])
def get_books():

    try:
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 1
        end = start + 1

        books = Book.query.all()

        if int(page) > len(books):
            abort(404)
        else:
            formatted_book = []
            for book in books:
                formatted_book.append(book.format())

            return jsonify({
                'books': formatted_book[start:end],
                'status':200,
                "all_book":len(books)
            })
    except:
        abort(404)

@app.route('/books/', methods=['POST'])
def add_book():

    try:
        body = request.get_json()

        author = body.get('author', None)
        title = body.get('title', None)
        rating = body.get('rating', None)

        book = Book(author=author, title=title, rating=rating)
        book.insert()

        return jsonify({
            'message': 'success',
            'status': 200
        })
    except:
        abort(404)
    

@app.route('/books/<int:book_id>/', methods=['GET'])
def get_book(book_id):
    try:
        book = Book.query.filter_by(id=book_id).first()

        return jsonify({
            'book':book.format(),
            'status': 200
        })
    except:
        abort(404)

@app.route('/books/<int:book_id>', methods=['PUT'])
def modify_book(book_id):
    try:
        body = request.get_json()

        author = body.get('author', None)
        title = body.get('title', None)
        rating = body.get('rating', None)

        book = Book.query.filter_by(id=book_id).first()

        book.author = author
        book.title = title
        book.rating = int(rating)
        book.update()

        return jsonify({
            "message": "success",
            "status": 200
        })
    except:
        abort(404)

@app.route('/books/<int:book_id>/', methods=['DELETE'])
def remove_book(book_id):
    
    book = Book.query.filter_by(id=book_id).first()

    book.delete()

    return jsonify({
        "message": "success",
        "status": 200
    })


# Error Handelers

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "message": "not found",
        "status": 404
    }), 404

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "message": "internal server error",
        "status": 500
    }), 500
