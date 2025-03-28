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
    if not all(key in data for key in ['name', 'lastname', 'email', 'password', 'im', 'role']):
        return jsonify({'message': 'Données manquantes'}), 400

    if data['role'] not in UserRole.__members__:
        return jsonify({'message': 'Role invalide'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email déjà utilisé"}), 400
        
    if User.query.filter_by(im=data['im']).first():
        return jsonify({"error": "Numéro matricule déjà utilisé"}), 400

    # Hachage du mot de passe
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        name=data['name'],
        lastname=data['lastname'],
        email=data['email'],
        im=data['im'],
        password=hashed_password,
        role=UserRole[data['role']],
        classe_id= data['classe_id']
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
            "name": new_user.name,
            "lastname": new_user.lastname,
            "email": new_user.email,
            "role": new_user.role.value
            
        },
        "token": generate_token(new_user)
    }), 201

# Connexion d'un utilisateur
def login_user(data):
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'message': 'Données manquantes'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    if check_password_hash(user.password, data['password']):
        token = generate_token(user)
        
        return jsonify({
            "message": "Connexion réussie",
            "user": {
                "id": user.id,
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "role": user.role.value
            },
            "token": token
        }), 200
    
    return jsonify({"error": "Mot de passe incorrect"}), 401

# Fonction utilitaire pour générer un token
def generate_token(user):
    return jwt.encode({
        'user_id': user.id,
        'role': user.role.value,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

# Profil de l'utilisateur protégé par le token
@token_required
def get_user_profile(current_user):
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "role": current_user.role.value
    }), 200
