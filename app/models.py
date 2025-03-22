from app import db

#definir une type enum pour le user
class UserRole(enum.Enum):
    ADMIN = 'admin'
    ENSEIGNANT:'enseignant'
    ETUDIANT:'etudiant'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=true)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)