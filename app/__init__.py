from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

db = SQLAlchemy()

# Charger les variables d'environnement
load_dotenv()

def create_app():
    app = Flask(__name__)

    #configuration de la base de donnees
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initialisation de la BD
    db.init_app(app)

    #importer les Blueprint
    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes,url_prefix='/api/users')

    return app