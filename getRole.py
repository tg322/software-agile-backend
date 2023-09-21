from app import app, db
from flask import jsonify, request

def get_all_roles():
    from models import roles
    userRoles = roles.query.all()

    all_userRoles = []

    if userRoles:
        for userRole in userRoles:
            all_userRoles.append({
                'id': userRole.id,
                'role': userRole.role_name
            })
        return all_userRoles
    else:
        return None

@app.route('/roles', methods=['GET'])
def runRoles():
    # data = request.get_json()
    all_userRoles = get_all_roles()
    

    if all_userRoles:
        return jsonify(all_userRoles)
    else:
        return jsonify({'message': 'Error accessing roles'}), 404