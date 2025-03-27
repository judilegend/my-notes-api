from app import db

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    niveau = db.Column(db.String(50), nullable=False)
    # filiere = db.Column(db.String(50), nullable=False)
    # annee_academique = db.Column(db.String(50), nullable=False)
    # professeur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # professeur = db.relationship('User', backref='classes')

    #Relation

    etudiants = db.relationship('User', backref='classe', lazy=True)
    modules = db.relationship('Module', secondary='classe_module',backref='classes', lazy=True)

    def __repr__(self):
        return f'<Classe {self.nom} - {self.niveau}>'