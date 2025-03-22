from app import db
from app.models.user import User,UserRole
from werkzeug.security import generate_password_hash , check_password_hash

from flask import jsonify

def register_user(data):
    #verifier si le role est valide
    if data['role'] not in UserRole.__members__:
        return jsonify({'message': 'Role invalide'}), 400

    # Vérifie si l’utilisateur existe déjà
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Nom d’utilisateur déjà pris"}), 400

    # Hash du mot de passe
    hashed_password = generate_password_hash(data['password'])

    # Crée un nouvel utilisateur
    new_user = User(
        username=data['username'],
        password=hashed_password,
        role=UserRole[data['role']]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur enregistré avec succès"}), 201

def login_user(data):
    # Vérifie si l’utilisateur existe
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "Nom d’utilisateur ou mot de passe incorrect"}), 401

    # Vérifie le mot de passe
    if not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Nom d’utilisateur ou mot de passe incorrect"}), 401
   # Génère un token JWT avec le SECRET_KEY
    token = jwt.encode({'user_id': user.id, 'role': user.role.name}, SECRET_KEY, algorithm='HS256')
    
    return jsonify({'token': token}), 200
    # return jsonify({"message": "Connexion réussie"}), 200
