import json
import jwt
import datetime
import os
from jwcrypto import jwe, jwk
from app import app, db

class encryption_key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypt_key = db.Column(db.String(250))

def get_key():
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

    print(decrypted_payload_dict)

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
        'exp': datetime.datetime.utcnow().timestamp() + 24 * 60 * 60
    }

    encryptedPayload = encrypt_payload(payload)

    new_payload = {'data': encryptedPayload}
    
    secret_key = 'your-secret-key'

    token = jwt.encode(new_payload, secret_key, algorithm='HS256')
    
    return token