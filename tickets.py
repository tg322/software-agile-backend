from app import app, db
from flask import jsonify, request
import bcrypt
from authentication import *

class tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_subject = db.Column(db.String(150))
    ticket_body = db.Column(db.String(3000))
    ticket_category = db.Column(db.Integer)
    ticket_from_id = db.Column(db.Integer)

def create_new_ticket(ticket_subject, ticket_body, ticket_category, ticket_from_id):
    new_ticket = tickets(ticket_subject=ticket_subject, ticket_body=ticket_body, ticket_category=ticket_category, ticket_from_id=ticket_from_id)
    db.session.add(new_ticket)
    db.session.commit()
    return 'check db'

@app.route('/newTicket', methods=['POST'])
def create_ticket():
    data = request.get_json()

    jwt_token = decodeToken(data['token'])

    decrypted_payload = decrypt_payload(jwt_token)

    user_id = decrypted_payload.get('user_id', None)

    response = create_new_ticket(data['ticketSubject'], data['ticketBody'], data['ticketCategory'], user_id)
    
    return jsonify(response)