from bookapp.app import app
from bookapp.models import user, db, book, bookread, globalvars
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


gvars = globalvars()

@app.errorhandler(404)
def not_found(e):  
  return {"Status": "Error", "result": "Page Not found !!"}, 404

@app.route("/")
def home():
    return {"Status": "Success","result": "Welcome to book logger!"}, 200 

@app.route("/signup", methods=["POST"])
def signup():
    params = request.json
    try:
        new_user = user(**params)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return {"Status": "Error", "result": "User already exists"}, 400
    return {"Status": "Success", "result": "New User created"},200


@app.route("/login", methods=["POST"])
def login():
    params = request.authorization
    if authenticate(params):
        return {"Status": "Success", "result": "User logged in"},200
    return {"Status": "Error", "result": "User not found"}, 400

@app.route("/logoff", methods=["POST"])
def logoff():
    gvars.guserid = -1
    return {"Status": "Success", "result": "User logged off "},200
    

def authenticate(params):
    # checks with the DB
    # returns if it's a valid user
    try:
        user_found = user.query.filter_by(username=params["username"]).first()
        if user_found is None:
            return False
        if user_found and user_found.password == params["password"]:
            gvars.guserid = user_found.uid
            gvars.gusertype = 0
            if user_found.is_reader:
                gvars.gusertype = 1
            return user_found.password == params["password"]
    except (KeyError, TypeError):
        return False


@app.route("/users", methods=["GET"])
def list_users():
    result = user.query.filter_by().all()
    response_list = []
    for uitem in result:
        response = {
                    "uid": uitem.uid, 
                    "firstname": uitem.firstname,
                    "lastname": uitem.lastname,
                    "usename":uitem.username,
                    "password":uitem.password,
                    "email":uitem.email,
                    "is_reader":uitem.is_reader
                    }
        response_list.append(response)
    return {"Status": "Success", "result": response_list}


@app.route("/book", methods=["GET"])
def list_books():
    result = book.query.filter_by().all()
    response_list = []
    for bitem in result:
        response = {
                    "bid": bitem.bid, 
                    "title": bitem.title,
                    "author": bitem.author,
                    "isbn":bitem.isbn
                    }
        response_list.append(response)
    return {"Status": "Success", "result": response_list}
    
# login required
# user type should be a adder user.is_reader = 0
@app.route("/book", methods=["POST"])
def add_book():
    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401
    if (gvars.gusertype == 1):
        return {"Status": "Error", "result": "UserType is Reader, Cannot add books"}, 401

    params = request.json
    for key in params:
        if key not in dir(book):
            return {"Status": "Error", "result": "Wrong input format"}, 401

    result = book(**params)
    result.user_id = gvars.guserid

    db.session.add(result)
    db.session.commit()

    return {"Status": "Success", "result": params}, 201

# login required
# user type should be a adder user.is_reader = 0
# Should not have any record in the book read table, for the book that is being deleted. 
@app.route("/book", methods=["DELETE"])
def remove_book():
    
    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401
    if (gvars.gusertype == 1):
        return {"Status": "Error", "result": "UserType is Reader, Cannot delete books"}, 401
      
    params = request.json
    bid = params["bid"]

    readbook_result = bookread.query.filter_by(book_id=bid).all()
    if len(readbook_result)>0 :
        return {"Status": "Error", "result": "Cannot delete this book- stars, reviews info exists"}, 401

    result = book.query.filter_by(bid=book_id).delete()
    db.session.commit()
    return {"Satatus":"Success","result":result}

@app.route("/book", methods=["PATCH"])
def update_book():
    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401
    if (gvars.gusertype == 1):
        return {"Status": "Error", "result": "UserType is Reader, Cannot edit books"}, 401
    
    params = request.json
    book_id = params["bid"]
    result = book.query.filter_by(bid=book_id).first()
    result.title = params["title"]
    result.author = params["author"]
    result.isbn = params["isbn"]
    result.user_id = gvars.guserid
    response = {
                    "bid": result.bid,
                    "title": result.title,
                    "author": result.author,
                    "isbn": result.isbn,
                    "user_id":result.user_id
                }
    db.session.commit()
    return {"Satatus":"Success","result":response}


@app.route("/readbook/all", methods=["GET"])
def read_books():
    result = bookread.query.filter_by().all()
    response_list = []
    for bitem in result:
        response = {
                    "book_id": bitem.book_id, 
                    "user_id": bitem.user_id,
                    "id": bitem.id,
                    "stars":bitem.stars,
                    "review":bitem.review
                    }
        response_list.append(response)
    
    return {"Status": "Success", "result": response_list}

# Should login
@app.route("/readbook/<b_id>",methods=["POST"])
def read_book(b_id):

    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401

    result = bookread.query.filter_by(book_id=b_id).all()
    if len(result)>0:
        for readitem in result:
            if (readitem.user_id == gvars.guserid):
                return {"Status": "Error", "result": "This book is already read, You can review the book"}, 401
   
    params={
                "user_id":gvars.guserid,
                "book_id":b_id
            }
    new_bookread = bookread(**params)
    db.session.add(new_bookread)
    db.session.commit()
    return {"Satatus":"Success","result":"Enjoy reading your book"},200

# Should login
# star review book - that is already read  in  /readbook/<b_id>
@app.route("/readbook/<b_id>",methods=["PATCH"])
def starreview_book(b_id):
    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401
    params = request.json
    result = bookread.query.filter_by(book_id=b_id).all()
    if len(result)>0:
        for readitem in result:
            if (readitem.user_id == gvars.guserid):  
                readitem.stars = params["stars"]
                readitem.review = params["review"]
                db.session.commit()
                return {"Satatus":"Success","result":"Thanks for reviewing"},200
    return {"Status": "Error", "result": "Please Read before You can review the book"}, 401


# Should login
# All books read by the user_id
@app.route("/readbook",methods=["GET"])
def read_book_list():
    if (gvars.guserid  < 0):
        return {"Status": "Error", "result": "Please login"}, 401

    result = bookread.query.filter_by(user_id=gvars.guserid).all()
    response_list = []
    for bitem in result:
        response = {
                    "book_id": bitem.book_id, 
                    "user_id": bitem.user_id,
                    "id": bitem.id,
                    "stars":bitem.stars,
                    "review":bitem.review
                    }
        response_list.append(response)
    
    return {"Status": "Success", "result": response_list}


# All stars and review on a book 
@app.route("/readbook/<b_id>",methods=["GET"])
def book_review_list(b_id):
    result = bookread.query.filter_by(book_id=b_id).all()
    response_list = []
    for bitem in result:
        response = {
                    "book_id": bitem.book_id, 
                    "user_id": bitem.user_id,
                    "id": bitem.id,
                    "stars":bitem.stars,
                    "review":bitem.review
                    }
        response_list.append(response)
    
    return {"Status": "Success", "result": response_list}
