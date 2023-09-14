from app import app, db
from flask import jsonify, request
import bcrypt
from authentication import *

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100))
    PassHash = db.Column(db.String(250))
    Role = db.Column(db.Integer)

class ticket_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))

class tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_subject = db.Column(db.String(150))
    ticket_body = db.Column(db.String(3000))
    ticket_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    ticket_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    ticket_category = db.relationship('Category', lazy='joined')
    user = db.relationship('User', lazy='joined')

    def serialize(self):
        return {
            'id': self.id,
            'ticket_subject': self.ticket_subject,
            'ticket_body': self.ticket_body,
            'ticket_category': self.ticket_category,
            'ticket_from_id': self.ticket_from_id
        }

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

@app.route('/getTickets', methods=['POST'])
def get_tickets():
    data = request.get_json()

    if verify_token(data['token']) == False:
        all_tickets = tickets.query.join(Category, Ticket.ticket_category_id == Category.id)\
                          .join(Users, Ticket.user_id == Users.id).all()
    
    
    return jsonify([ticket.serialize() for ticket in all_tickets])