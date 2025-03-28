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
 # Importer les Blueprint
    from app.routes.user_routes import user_routes
    from app.routes.classe_routes import classe_routes
    from app.routes.semestre_routes import semestre_routes
    from app.routes.module_routes import module_routes
    from app.routes.note_routes import note_routes
    from app.routes.reclamation_routes import reclamation_routes

  # Enregistrer les Blueprint
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(classe_routes, url_prefix='/api/classes')
    app.register_blueprint(semestre_routes, url_prefix='/api/semestres')
    app.register_blueprint(module_routes, url_prefix='/api/modules')
    app.register_blueprint(note_routes, url_prefix='/api/notes')
    app.register_blueprint(reclamation_routes, url_prefix='/api/reclamations')

    return app
