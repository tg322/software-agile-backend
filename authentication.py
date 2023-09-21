import json
import jwt
import datetime
import os
from jwcrypto import jwe, jwk
from app import app, db


def get_key():
    from models import encryption_key
    key_data = encryption_key.query.first()
    if key_data:
        return key_data.encrypt_key
    else:
        return None 
    
def decrypt_payload(payload):
    jwetoken = jwe.JWE()

    key_str = get_key()

    key_dict = json.loads(key_str)

    key = jwk.JWK(**key_dict)

    jwetoken.deserialize(payload, key=key)
    
    decrypted_payload = jwetoken.payload.decode('utf-8')

    decrypted_payload_dict = json.loads(decrypted_payload)

    return decrypted_payload_dict

def encrypt_payload(payload):

    payload_str = json.dumps(payload)

    key_str = get_key()

    key_dict = json.loads(key_str)

    key = jwk.JWK(**key_dict)

    jwetoken = jwe.JWE(plaintext=payload_str.encode('utf-8'),
                    protected={"alg": "A256KW", "enc": "A256CBC-HS512"})
    jwetoken.add_recipient(key)
    encrypted_payload = jwetoken.serialize(compact=True)

    decrypt_payload(encrypted_payload)

    return encrypted_payload

def create_token(user_data):
   
    payload = {
        'user_id': user_data['id'],
        'email': user_data['Email'],
        'permissionLevel': user_data['Role'],
        'exp': datetime.datetime.utcnow().timestamp() + 24 * 60 * 60
    }

    encryptedPayload = encrypt_payload(payload)

    new_payload = {'data': encryptedPayload}
    
    secret_key = 'your-secret-key'

    token = jwt.encode(new_payload, secret_key, algorithm='HS256')
    
    return token

def decodeToken(token_str):
    secret_key = 'your-secret-key'
    decoded_jwt = jwt.decode(token_str, secret_key, algorithms=['HS256'])
    jwe_payload = decoded_jwt.get('data', None)
    
    # If 'data' is not in the JWT, return False
    if jwe_payload is None:
        return False
    return jwe_payload

def verify_token(token_str):
    
    jwe_payload = decodeToken(token_str)
    
    # Decrypt the JWE payload
    decrypted_payload = decrypt_payload(jwe_payload)
    
    # Extract the 'exp' timestamp and compare it to the current time
    exp_timestamp = decrypted_payload.get('exp', None)
    if exp_timestamp is None:
        return False
    # if datetime.datetime.utcnow().timestamp() <= exp_timestamp:
    permissionLevel = decrypted_payload.get('permissionLevel', None)
    if permissionLevel is None:
        return False
    isAdmin = checkIfAdmin(permissionLevel)

    tokenIsValid = datetime.datetime.utcnow().timestamp() <= exp_timestamp

    response = {
        'permissionLevel': isAdmin,
        'tokenIsValid': tokenIsValid
    }

    return response


def checkIfAdmin(roleID):
    from models import roles
    role = roles.query.filter_by(id=roleID).first()

    if role.role_name == 'Admin':
        return True
    
    return False
