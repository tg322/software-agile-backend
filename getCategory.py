from app import app, db
from flask import jsonify, request

def get_all_categories():
    from models import ticket_category
    categories = ticket_category.query.all()

    all_categories = []

    if categories:
        for category in categories:
            all_categories.append({
                'id': category.id,
                'category': category.category
            })
        return all_categories
    else:
        return None

@app.route('/categories', methods=['GET'])
def runCategories():
    # data = request.get_json()
    allCategories = get_all_categories()
    

    if allCategories:
        return jsonify(allCategories)
    else:
        return jsonify({'message': 'Error accessing categories'}), 404