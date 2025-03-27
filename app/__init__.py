from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import secrets

db = SQLAlchemy()

# Charger les variables d'environnement
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration CORS plus précise
    CORS(app, resources={r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})
    
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Définir une clé secrète pour l'application
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))

    # Initialisation de la BD
    db.init_app(app)

    # Importer les Blueprint
    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes, url_prefix='/api/users')

    return app
