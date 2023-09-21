from app import app, db
from flask import jsonify, request
import bcrypt
from authentication import *


# Create User Method---------------------------------------------------------------------------------
def insert_user(Email, PassHash, Role, fName, Lname):
    from models import users
    new_user = users(first_name=fName, last_name=Lname, Email=Email, PassHash=PassHash, Role=Role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Email': new_user.Email, 'PassHash': new_user.PassHash, 'Role': new_user.Role})

# Create User route
@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    password = data['password'].encode('utf-8')
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    response = insert_user(data['userEmail'], hash, data['userRole'], data['fName'], data['lName'])
    return response
# ---------------------------------------------------------------------------------------------------


def get_user_by_email(email):
    from models import users

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
            permissionLevel = checkIfAdmin(user_data['Role'])
            response = {
                'token': token,
                'permissionLevel': permissionLevel
            }

            return jsonify(response)
        else:
            return jsonify({'message': 'failed'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    

@app.route('/verify-token', methods=['POST'])
def runVerify():
    data = request.get_json()
    print(data['token'])
    tokenValidation = verify_token(data['token'])
    if tokenValidation['tokenIsValid']:
        return jsonify(tokenValidation)


    return jsonify({'message': 'Token Error'}), 404
        