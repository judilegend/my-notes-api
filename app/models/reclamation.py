from app import db
import enum
import datetime

class StatutReclamation(enum.Enum):
    EN_ATTENTE = 'en_attente'
    VALIDEE_ENSEIGNANT = 'validee_enseignant'
    REJETEE_ENSEIGNANT = 'rejetee_enseignant'
    VALIDEE_ADMIN = 'validee_admin'
    REJETEE_ADMIN = 'rejetee_admin'

class Reclamation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_traitement = db.Column(db.DateTime, nullable=True)
    statut = db.Column(db.Enum(StatutReclamation), default=StatutReclamation.EN_ATTENTE)
    commentaire_enseignant = db.Column(db.Text, nullable=True)
    commentaire_admin = db.Column(db.Text, nullable=True)
    
    # Clés étrangères
    etudiant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    
    def __repr__(self):
        return f'<Reclamation {self.id} - Statut: {self.statut.value}>'
