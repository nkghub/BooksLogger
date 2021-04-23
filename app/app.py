
# load db url from the env variable. you can use python-dotenv package

from flask import Flask, request
from dotenv import load_dotenv
import os

import models

load_dotenv()
db_url = os.environ["DATABASE_URL"]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



@app.route("/")
def home():
    return {"Status": "Success"}, 200 


@app.route("/book")
def list_books():
    print("**** LIST BOOK")
    result = models.book.query.filter_by().all()
    print ("*****",len(result))

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

@app.route("/addbook", methods=["POST"])
def add_book():
    params = request.json
    for key in params:
        if key not in dir(models.book):
            return {"Status": "Error", "result": "Wrong input format"}, 401
    result = models.book(**params)
    models.db.session.add(result)
    models.db.session.commit()
    
    return {"Status": "Success", "result": params}, 201

@app.route("/removebook", methods=["POST"])
def remove_book():
    params = request.json
    book_id = params["bid"]
    result = models.book.query.filter_by(bid=book_id).delete()
    print("Book deleted with bid =", book_id)
    models.db.session.commit()
    return {"Satatus":"Success","result":result}

@app.route("/updatebook", methods=["POST"])
def update_book():
    print("**** In Update Book ***")
    params = request.json
    book_id = params["bid"]
    result = models.book.query.filter_by(bid=book_id).first()
    result.title = params["title"]
    result.author = params["author"]
    result.isbn = params["isbn"]
    response = {
                    "bid": result.bid,
                    "title": result.title,
                    "author": result.author,
                    "isbn": result.isbn
                }
    print("Book updated  with bid =", book_id)
    models.db.session.commit()
    return {"Satatus":"Success","result":response}




# Run the app in port 5000 and in debug mode
if __name__ == '__main__':
    models.db.create_all()
    models.db.init_app(app)
    app.run(port=5000, debug=True)