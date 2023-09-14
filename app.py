# from flask import Flask, jsonify, request
# import bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from jwcrypto import jwe, jwk
# import os

# app = Flask(__name__)
# CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software-agile'

# db = SQLAlchemy(app)

# class users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Email = db.Column(db.String(100))
#     PassHash = db.Column(db.String(250))
#     Role = db.Column(db.Integer)

# def create_user(Email, PassHash, Role):
#     new_user = users(Email=Email, PassHash=PassHash, Role=Role)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'Email': new_user.Email, 'PassHash': new_user.PassHash, 'Role': new_user.Role})

# def check_password(plain_text_password, hashed_password):
    
#     return bcrypt.checkpw(plain_text_password, hashed_password)


# @app.route('/users', methods=['POST'])
# def runUser():
#     hash = bcrypt.hashpw(b'testAdmin', bcrypt.gensalt())
#     response = create_user('testAdmin@test.com', hash, 1)
#     return response

# def get_user_by_email(email):
#     user = users.query.filter_by(Email=email).first()
#     if user:
#         return{
#             'Email': user.Email,
#             'PassHash': user.PassHash,
#             'Role': user.Role
#         }
#     else:
#         return None
    
# def encrypt_payload(payload):
#     key_value = os.getenv('ENCRYPTION_KEY')
#     key = jwk.JWK(k=key_value, kty='oct')
#     jwetoken = jwe.JWE(payload.encode('utf-8'), json_encode=True)
#     jwetoken.add_recipient(key)
#     encrypted_payload = jwetoken.serialize()

#     return encrypted_payload




# @app.route('/login', methods=['POST'])
# def runLogin():
#     data = request.get_json()
#     user_data = get_user_by_email(data['email'])

#     if user_data:
#         pass_hash = user_data['PassHash']
        
#         if check_password(data['password'], pass_hash):
#             return jsonify({'key': 'something'})
#         else:
#             return jsonify({'message': 'failed'})
#     else:
#         return jsonify({'message': 'User not found'}), 404

    



# if __name__ == '__main__':
    
#     app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software-agile'

db = SQLAlchemy(app)

# Import routes from other modules
from userAccess import *
from tickets import *
from getCategory import *

if __name__ == '__main__':
    app.run(debug=True)