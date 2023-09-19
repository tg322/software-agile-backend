from sqlalchemy.orm import aliased
from app import app, db
from flask import jsonify, request

from authentication import *

def create_new_ticket(ticket_subject, ticket_body, ticket_category, ticket_from_id):
    from models import Tickets
    try:
        new_ticket = Tickets(
            ticket_subject=ticket_subject, 
            ticket_body=ticket_body, 
            ticket_category=ticket_category, 
            ticket_from_id=ticket_from_id
        )
        db.session.add(new_ticket)
        db.session.commit()
        return 'Ticket created successfully.'
    except Exception as e:
        db.session.rollback()
        return f'An error occurred: {e}'

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
    from models import Tickets, ticket_category, users
    data = request.get_json()

    category_alias = aliased(ticket_category)
    user_alias = aliased(users)

    all_tickets = []

    response = {}
    if verify_token(data['token']):
        all_tickets = db.session.query(Tickets, category_alias, user_alias)\
        .join(category_alias, Tickets.ticket_category == category_alias.id)\
        .join(user_alias, Tickets.ticket_from_id == user_alias.id).all()
        
        serialized_data = [
        {
            'ticket_id': ticket.id,
            'ticket_subject': ticket.ticket_subject,
            'category': category.category,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ticket_date': ticket.ticket_date_sent,
            'ticket_status': ticket.ticket_status,
        }
        for ticket, category, user in all_tickets
        ]

        response = {'tickets': serialized_data}

        print(response)

        return jsonify(response)
    
    return jsonify({"error": "Invalid token"})


@app.route('/getOpenTickets', methods=['POST'])
def getOpenTickets():
    from models import Tickets, ticket_category, users
    data = request.get_json()

    category_alias = aliased(ticket_category)
    user_alias = aliased(users)

    all_tickets = []

    response = {}
    if verify_token(data['token']):
        all_tickets = db.session.query(Tickets, category_alias, user_alias)\
        .join(category_alias, Tickets.ticket_category == category_alias.id)\
        .join(user_alias, Tickets.ticket_from_id == user_alias.id).filter(Tickets.ticket_status == 'Open').all()
        
        serialized_data = [
        {
            'ticket_id': ticket.id,
            'ticket_subject': ticket.ticket_subject,
            'category': category.category,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ticket_date': ticket.ticket_date_sent,
            'ticket_status': ticket.ticket_status,
        }
        for ticket, category, user in all_tickets
        ]

        response = {'tickets': serialized_data}

        print(response)

        return jsonify(response)
    
    return jsonify({"error": "Invalid token"})



@app.route('/getTicketById', methods=['POST'])
def getTicketById():
    from models import Tickets, ticket_category, users
    data = request.get_json()
    
    print("Received ID:", data['id'])  # Debug print

    category_alias = aliased(ticket_category)
    user_alias = aliased(users)

    if verify_token(data['token']):
        ticket = db.session.query(Tickets, category_alias, user_alias)\
            .join(category_alias, Tickets.ticket_category == category_alias.id)\
            .join(user_alias, Tickets.ticket_from_id == user_alias.id)\
            .filter(Tickets.id == data['id']).first()

        print("Query result:", ticket)  # Debug print

        if ticket is None:
            return jsonify({"error": "Ticket not found"})

        ticket, category, user = ticket

        serialized_data = {
            'ticket_id': ticket.id,
            'ticket_subject': ticket.ticket_subject,
            'ticket_body': ticket.ticket_body,
            'category': category.category,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ticket_date': ticket.ticket_date_sent,
            'ticket_status': ticket.ticket_status,
        }

        return jsonify({'ticket': serialized_data})
    
    return jsonify({"error": "Invalid token"})

@app.route('/deleteTicket', methods=['POST'])
def deleteTicketByID():
    from models import Tickets
    data = request.get_json()

    if verify_token(data['token']):
        Tickets.query.filter(Tickets.id == data['id']).delete()
        db.session.commit()
        return jsonify({"Success": "Ticket Deleted"})
    return jsonify({"error": "Invalid token"})

@app.route('/closeTicket', methods=['POST'])
def closeTicketByID():
    from models import Tickets
    data = request.get_json()

    if verify_token(data['token']):
        ticket = Tickets.query.get(data['id'])
        ticket.ticket_status = 'Closed'
        db.session.commit()
        return jsonify({"Success": "Ticket Closed"})
    return jsonify({"error": "Invalid token"})
