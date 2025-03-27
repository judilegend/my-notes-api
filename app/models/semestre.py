from app import db
import enum

class SemestreType(enum.Enum):
    S1 = 'Semestre 1'
    S2 = 'Semestre 2'
    S3 = 'Semestre 3'
    S4 = 'Semestre 4'
    S5 = 'Semestre 5'
    S6 = 'Semestre 6'
    S7: 'Semestre 7'

class Semestre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(SemestreType), nullable=False)
    annee_academique = db.Column(db.String(20), nullable=False)  # Ex: 2023-2024
    
    # Relations
    modules = db.relationship('Module', backref='semestre', lazy=True)
    
    def __repr__(self):
        return f'<Semestre {self.type.value} - {self.annee_academique}>'
