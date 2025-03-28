from flask import Blueprint,request

from app.controllers.user_controller import register_user,login_user,get_user_profile

#creation de Blueprint
user_routes = Blueprint('user_routes', __name__)

#route pour enregistrer un utilisateur
@user_routes.route('/register', methods=['POST'])

def register():
    data = request.get_json()
    return register_user(data)

#route pour se connecter 
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

# Route pour obtenir le profil de l'utilisateur connecté
@user_routes.route('/profile', methods=['GET'])
def profile():
    return get_user_profile()