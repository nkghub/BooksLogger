
#load db url from the env variable. you can use python-dotenv package

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, make_response
from dotenv import load_dotenv
import os

print(os.environ.get('PYTHONPATH', ''))

load_dotenv()
db_url = os.environ["DATABASE_URL"]

#db_url = db_url.replace('postgres', 'postgresql', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


from bookapp.views import *
from flask_jwt import JWT, jwt_required, current_identity


# Run the app in port 5000 and in debug mode
if __name__ == '__main__':
    app.run(port=5000, debug=True)
