from app import db
from app.models.user import User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import jsonify, current_app, request
from functools import wraps

# Middleware pour protéger les routes avec un token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            print("[DEBUG] Token manquant")
            return jsonify({'message': 'Token manquant!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            print(f"[DEBUG] Erreur de token: {e}")
            return jsonify({'message': 'Token invalide!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

# Enregistrement d'un nouvel utilisateur
def register_user(data):
    if not all(key in data for key in ['username', 'password', 'role']):
        return jsonify({'message': 'Données manquantes'}), 400

    if data['role'] not in UserRole.__members__:
        return jsonify({'message': 'Role invalide'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400

    # Hachage du mot de passe
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        username=data['username'],
        password=hashed_password,
        role=UserRole[data['role']]
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de l'enregistrement: {str(e)}"}), 500

    return jsonify({
        "message": "Utilisateur enregistré avec succès",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role.value
        }
    }), 201

# Connexion d'un utilisateur
def login_user(data):
    if not all(key in data for key in ['username', 'password']):
        return jsonify({'message': 'Données manquantes'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role.value,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "message": "Connexion réussie",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role.value
            },
            "token": token
        }), 200
    
    return jsonify({"error": "Mot de passe incorrect"}), 401

# Profil de l'utilisateur protégé par le token
@token_required
def get_user_profile(current_user):
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role.value
    }), 200
