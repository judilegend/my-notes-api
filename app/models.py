from app import db

class Etudiant(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'note': self.note
        }
