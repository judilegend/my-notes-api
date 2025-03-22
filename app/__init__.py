from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #configuration de la base de donnees
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initialisation de la BD
    db.init_app(app)

    #importer les routes
    from app.routes import main
    app.register_blueprint(main)

    return app