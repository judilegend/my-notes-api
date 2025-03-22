from app import db
from app.models import Etudiant

def ajouter_etudiant(nom, note):
    nouvel_etudiant = Etudiant(nom=nom, note=note)
    db.session.add(nouvel_etudiant)
    db.session.commit()
    return nouvel_etudiant

def obtenir_tous_les_etudiants():
    return Etudiant.query.all()

def obtenir_etudiant_par_id(eleve_id):
    return Etudiant.query.get(eleve_id)

def mettre_a_jour_etudiant(eleve_id, nom=None, note=None):
    etudiant = Etudiant.query.get(eleve_id)
    if etudiant:
        if nom:
            etudiant.nom = nom
        if note is not None:
            etudiant.note = note
        db.session.commit()
    return etudiant

def supprimer_etudiant(eleve_id):
    etudiant = Etudiant.query.get(eleve_id)
    if etudiant:
        db.session.delete(etudiant)
        db.session.commit()
    return etudiant
