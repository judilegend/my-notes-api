import enum
from app import db

class UserRole(enum.Enum):
    ADMIN = 'admin'
    ENSEIGNANT = 'enseignant'
    ETUDIANT = 'etudiant'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Ajout du champ email
    im = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
