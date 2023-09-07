from app import app, db
from flask import jsonify, request

class ticket_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))

def get_all_categories():
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