from app import db
from app.models.notes import Note
from app.models.module import Module
from app.models.user import User, UserRole
from app.controllers.user_controller import token_required
from flask import jsonify, request
import datetime

# Ajouter une note (Admin ou Enseignant)
@token_required
def add_note(current_user, data):
    if current_user.role not in [UserRole.ADMIN, UserRole.ENSEIGNANT]:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if not all(key in data for key in ['etudiant_id', 'module_id']):
        return jsonify({'message': 'Données manquantes'}), 400
    
    # Vérifier si l'étudiant existe
    etudiant = User.query.get(data['etudiant_id'])
    if not etudiant or etudiant.role != UserRole.ETUDIANT:
        return jsonify({'message': 'Étudiant non trouvé'}), 404
    
    # Vérifier si le module existe
    module = Module.query.get(data['module_id'])
    if not module:
        return jsonify({'message': 'Module non trouvé'}), 404
    
    # Si l'utilisateur est un enseignant, vérifier qu'il enseigne ce module
    if current_user.role == UserRole.ENSEIGNANT and module.enseignant_id != current_user.id:
        return jsonify({'message': 'Vous n\'êtes pas autorisé à ajouter des notes pour ce module'}), 403
    
    # Vérifier si une note existe déjà pour cet étudiant et ce module
    existing_note = Note.query.filter_by(etudiant_id=data['etudiant_id'], module_id=data['module_id']).first()
    if existing_note:
        return jsonify({'message': 'Une note existe déjà pour cet étudiant dans ce module'}), 400
    
    # Créer la nouvelle note
    new_note = Note(
        etudiant_id=data['etudiant_id'],
        module_id=data['module_id'],
        note_theorique=data.get('note_theorique'),
        note_pratique=data.get('note_pratique')
    )
    
    # Calculer la moyenne
    new_note.calculer_moyenne()
    
    try:
        db.session.add(new_note)
        db.session.commit()
        return jsonify({
            'message': 'Note ajoutée avec succès',
            'note': {
                'id': new_note.id,
                'etudiant_id': new_note.etudiant_id,
                'module_id': new_note.module_id,
                'note_theorique': new_note.note_theorique,
                'note_pratique': new_note.note_pratique,
                'moyenne': new_note.moyenne,
                'date_ajout': new_note.date_ajout.isoformat() if new_note.date_ajout else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de l\'ajout de la note: {str(e)}'}), 500

# Mettre à jour une note (Admin ou Enseignant)
@token_required
def update_note(current_user, note_id, data):
    if current_user.role not in [UserRole.ADMIN, UserRole.ENSEIGNANT]:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    note = Note.query.get_or_404(note_id)
    
    # Si l'utilisateur est un enseignant, vérifier qu'il enseigne ce module
    if current_user.role == UserRole.ENSEIGNANT:
        module = Module.query.get(note.module_id)
        if module.enseignant_id != current_user.id:
            return jsonify({'message': 'Vous n\'êtes pas autorisé à modifier cette note'}), 403
    
    if 'note_theorique' in data:
        note.note_theorique = data['note_theorique']
    
    if 'note_pratique' in data:
        note.note_pratique = data['note_pratique']
    
    # Recalculer la moyenne
    note.calculer_moyenne()
    note.date_modification = datetime.datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Note mise à jour avec succès',
            'note': {
                'id': note.id,
                'etudiant_id': note.etudiant_id,
                'module_id': note.module_id,
                'note_theorique': note.note_theorique,
                'note_pratique': note.note_pratique,
                'moyenne': note.moyenne,
                'date_ajout': note.date_ajout.isoformat() if note.date_ajout else None,
                'date_modification': note.date_modification.isoformat() if note.date_modification else None
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la mise à jour de la note: {str(e)}'}), 500

# Obtenir toutes les notes (Admin uniquement)
@token_required
def get_all_notes(current_user):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    notes = Note.query.all()
    result = []
    
    for note in notes:
        result.append({
            'id': note.id,
            'etudiant_id': note.etudiant_id,
            'etudiant_nom': f"{note.etudiant.name} {note.etudiant.lastname}",
            'module_id': note.module_id,
            'module_nom': note.module.nom,
            'note_theorique': note.note_theorique,
            'note_pratique': note.note_pratique,
            'moyenne': note.moyenne,
            'date_ajout': note.date_ajout.isoformat() if note.date_ajout else None,
            'date_modification': note.date_modification.isoformat() if note.date_modification else None
        })
    
    return jsonify({'notes': result}), 200

# Obtenir les notes d'un étudiant spécifique
@token_required
def get_notes_by_etudiant(current_user, etudiant_id=None):
    # Si l'etudiant_id n'est pas fourni, utiliser l'ID de l'utilisateur actuel
    if etudiant_id is None:
        etudiant_id = current_user.id
    else:
        # Vérifier les permissions
        if current_user.role == UserRole.ETUDIANT and current_user.id != int(etudiant_id):
            return jsonify({'message': 'Vous ne pouvez consulter que vos propres notes'}), 403
    
    # Vérifier si l'étudiant existe
    etudiant = User.query.get(etudiant_id)
    if not etudiant or etudiant.role != UserRole.ETUDIANT:
        return jsonify({'message': 'Étudiant non trouvé'}), 404
    
    notes = Note.query.filter_by(etudiant_id=etudiant_id).all()
    result = []
    
    for note in notes:
        module = Module.query.get(note.module_id)
        result.append({
            'id': note.id,
            'module_id': note.module_id,
            'module_nom': module.nom,
            'module_code': module.code,
            'credits': module.credits,
            'semestre': module.semestre.type.value if module.semestre else None,
            'annee_academique': module.semestre.annee_academique if module.semestre else None,
            'note_theorique': note.note_theorique,
            'note_pratique': note.note_pratique,
            'moyenne': note.moyenne,
            'date_ajout': note.date_ajout.isoformat() if note.date_ajout else None,
            'date_modification': note.date_modification.isoformat() if note.date_modification else None
        })
    
    return jsonify({
        'etudiant': {
            'id': etudiant.id,
            'nom': etudiant.name,
            'prenom': etudiant.lastname,
            'im': etudiant.im
        },
        'notes': result
    }), 200

# Obtenir les notes pour un module spécifique
@token_required
def get_notes_by_module(current_user, module_id):
    # Vérifier si le module existe
    module = Module.query.get_or_404(module_id)
    
    # Vérifier les permissions
    if current_user.role == UserRole.ETUDIANT:
        # Les étudiants ne peuvent voir que leurs propres notes
        notes = Note.query.filter_by(module_id=module_id, etudiant_id=current_user.id).all()
    elif current_user.role == UserRole.ENSEIGNANT:
        # Les enseignants ne peuvent voir que les notes des modules qu'ils enseignent
        if module.enseignant_id != current_user.id:
            return jsonify({'message': 'Vous n\'êtes pas autorisé à consulter ces notes'}), 403
        notes = Note.query.filter_by(module_id=module_id).all()
    else:  # Admin
        notes = Note.query.filter_by(module_id=module_id).all()
    
    result = []
    for note in notes:
        etudiant = User.query.get(note.etudiant_id)
        result.append({
            'id': note.id,
            'etudiant_id': note.etudiant_id,
            'etudiant_nom': f"{etudiant.name} {etudiant.lastname}",
            'etudiant_im': etudiant.im,
            'note_theorique': note.note_theorique,
            'note_pratique': note.note_pratique,
            'moyenne': note.moyenne,
            'date_ajout': note.date_ajout.isoformat() if note.date_ajout else None,
            'date_modification': note.date_modification.isoformat() if note.date_modification else None
        })
    
    return jsonify({
        'module': {
            'id': module.id,
            'nom': module.nom,
            'code': module.code,
            'credits': module.credits
        },
        'notes': result
    }), 200

# Supprimer une note (Admin uniquement)
@token_required
def delete_note(current_user, note_id):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    note = Note.query.get_or_404(note_id)
    
    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note supprimée avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la suppression: {str(e)}'}), 500
