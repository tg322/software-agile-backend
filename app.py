

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import *

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software-agile'

db = SQLAlchemy(app)

# Import routes from other modules
from userAccess import *
from tickets import *
from getCategory import *
from getRole import *

if __name__ == '__main__':
    app.run(debug=True)