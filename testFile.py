from models import Tickets, ticket_category, users
from app import db
from sqlalchemy.orm import aliased

def test_query():
    category_alias = aliased(ticket_category)
    user_alias = aliased(users)

    ticket = db.session.query(Tickets, category_alias, user_alias)\
        .join(category_alias, Tickets.ticket_category == category_alias.id)\
        .join(user_alias, Tickets.ticket_from_id == user_alias.id)\
        .filter_by(id=4).first()

    print(ticket)

if __name__ == '__main__':
    test_query()