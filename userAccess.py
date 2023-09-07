from app import app, db
from flask import jsonify, request
import bcrypt
from authentication import *

# Database Models ----------------------------------------------------------------------------------
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100))
    PassHash = db.Column(db.String(250))
    Role = db.Column(db.Integer)

# --------------------------------------------------------------------------------------------------


# Create User Method---------------------------------------------------------------------------------
def create_user(Email, PassHash, Role):
    new_user = users(Email=Email, PassHash=PassHash, Role=Role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Email': new_user.Email, 'PassHash': new_user.PassHash, 'Role': new_user.Role})

# Create User route
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data['password']
    
    hash = bcrypt.hashpw(b'testAdmin', bcrypt.gensalt())
    response = create_user(data['email'], hash, data['role'])
    return response
# ---------------------------------------------------------------------------------------------------


def get_user_by_email(email):
    user = users.query.filter_by(Email=email).first()
    if user:
        return{
            'id': user.id,
            'Email': user.Email,
            'PassHash': user.PassHash,
            'Role': user.Role
        }
    else:
        return None
    
def check_password(plain_text_password, hashed_password):
    
    return bcrypt.checkpw(plain_text_password, hashed_password)



@app.route('/login', methods=['POST'])
def runLogin():
    data = request.get_json()
    user_data = get_user_by_email(data['email'])

    if user_data:
        pass_hash = user_data['PassHash']
        
        if check_password(data['password'], pass_hash):
            token = create_token(user_data)
            return jsonify(token)
        else:
            return jsonify({'message': 'failed'})
    else:
        return jsonify({'message': 'User not found'}), 404