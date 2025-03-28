from app import db

class Classe(db.Model):
    __tablename__ = 'classe'

    id = db.Column(db.Integer, primary_key=True)
    mention = db.Column(db.String(40), nullable=False)
    parcours = db.Column(db.String(200), nullable=False)
    niveau = db.Column(db.String(50), nullable=False)

    # Relations
    etudiants = db.relationship('User', backref='classe', lazy=True)  # Corrigé ici
    modules = db.relationship('Module', secondary='classe_module', backref='classes', lazy=True)

    def __repr__(self):
        return f'<Classe {self.nom} - {self.niveau}>'
