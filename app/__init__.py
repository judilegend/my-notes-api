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

    # Configuration CORS
    CORS(app, resources={r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))

    # Initialisation de la base de données
    db.init_app(app)

    # Importer les modèles pour éviter les erreurs d'importation circulaire
    with app.app_context():
        from app.models import user, classe,semestre, module, notes, reclamation
        db.create_all()

    # Importer les Blueprints
    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes, url_prefix='/api/users')

    return app
