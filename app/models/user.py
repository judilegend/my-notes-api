import enum
from app import db

class UserRole(enum.Enum):
    ADMIN = 'admin'
    ENSEIGNANT = 'enseignant'
    ETUDIANT = 'etudiant'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
