from flask import Flask, jsonify, json, request, Response

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat In the Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]

#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books' : books})

#GET /books/isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "new_book": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErroMessage = {
            "error": "Invalid book object passed in request",
            "helpString": ""
        }
        response = Response(json.dumps(invalidBookObjectErroMessage), status=400, mimetype='application/json')
        return response

@app.route('books/<int:isbn>', methods=['PUT'])
def update_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

@app.route('books//<int:isbn', methods=['PATCH'])
def patch_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books" + str(isbn)
    return response

app.run(port=5000)