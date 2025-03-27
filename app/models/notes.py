from app import db
import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_theorique = db.Column(db.Float, nullable=True)
    note_pratique = db.Column(db.Float, nullable=True)
    moyenne = db.Column(db.Float, nullable=True)
    date_ajout = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modification = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    
    # Clés étrangères
    etudiant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    
    # Relations
    reclamations = db.relationship('Reclamation', backref='note', lazy=True)
    
    def __repr__(self):
        return f'<Note {self.id} - Étudiant: {self.etudiant_id} - Module: {self.module_id}>'
    
    def calculer_moyenne(self):
        if self.note_theorique is not None and self.note_pratique is not None:
            self.moyenne = (self.note_theorique + self.note_pratique) / 2
        elif self.note_theorique is not None:
            self.moyenne = self.note_theorique
        elif self.note_pratique is not None:
            self.moyenne = self.note_pratique
        else:
            self.moyenne = None
        return self.moyenne
