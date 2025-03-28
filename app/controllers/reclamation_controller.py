from app import db
from app.models.reclamation import Reclamation, StatutReclamation
from app.models.notes import Note
from app.models.module import Module
from app.models.user import User, UserRole
from app.controllers.user_controller import token_required
from flask import jsonify, request
import datetime

# Créer une réclamation (Étudiant)
@token_required
def create_reclamation(current_user, data):
    if current_user.role != UserRole.ETUDIANT:
        return jsonify({'message': 'Seuls les étudiants peuvent créer des réclamations'}), 403
    
    if not all(key in data for key in ['note_id', 'description']):
        return jsonify({'message': 'Données manquantes'}), 400
    
    # Vérifier si la note existe et appartient à l'étudiant
    note = Note.query.get(data['note_id'])
    if not note:
        return jsonify({'message': 'Note non trouvée'}), 404
    
    if note.etudiant_id != current_user.id:
        return jsonify({'message': 'Vous ne pouvez pas créer de réclamation pour cette note'}), 403
    
    # Vérifier si une réclamation existe déjà pour cette note
    existing_reclamation = Reclamation.query.filter_by(note_id=data['note_id'], etudiant_id=current_user.id).first()
    if existing_reclamation:
        return jsonify({'message': 'Une réclamation existe déjà pour cette note'}), 400
    
    new_reclamation = Reclamation(
        description=data['description'],
        etudiant_id=current_user.id,
        note_id=data['note_id'],
        statut=StatutReclamation.EN_ATTENTE
    )
    
    try:
        db.session.add(new_reclamation)
        db.session.commit()
        return jsonify({
            'message': 'Réclamation créée avec succès',
            'reclamation': {
                'id': new_reclamation.id,
                'description': new_reclamation.description,
                'date_creation': new_reclamation.date_creation.isoformat(),
                'statut': new_reclamation.statut.value,
                'note_id': new_reclamation.note_id
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la création: {str(e)}'}), 500

# Obtenir toutes les réclamations (Admin)
@token_required
def get_all_reclamations(current_user):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    reclamations = Reclamation.query.all()
    result = []
    
    for reclamation in reclamations:
        etudiant = User.query.get(reclamation.etudiant_id)
        note = Note.query.get(reclamation.note_id)
        module = Module.query.get(note.module_id) if note else None
        
        result.append({
            'id': reclamation.id,
            'description': reclamation.description,
            'date_creation': reclamation.date_creation.isoformat(),
            'date_traitement': reclamation.date_traitement.isoformat() if reclamation.date_traitement else None,
            'statut': reclamation.statut.value,
            'commentaire_enseignant': reclamation.commentaire_enseignant,
            'commentaire_admin': reclamation.commentaire_admin,
            'etudiant': {
                'id': etudiant.id,
                'nom': f"{etudiant.name} {etudiant.lastname}",
                'im': etudiant.im
            },
            'note': {
                'id': note.id,
                'module': module.nom if module else 'Module inconnu',
                'note_theorique': note.note_theorique,
                'note_pratique': note.note_pratique,
                'moyenne': note.moyenne
            } if note else None
        })
    
    return jsonify({'reclamations': result}), 200

# Obtenir les réclamations d'un étudiant
@token_required
def get_reclamations_by_etudiant(current_user, etudiant_id=None):
    # Si l'etudiant_id n'est pas fourni, utiliser l'ID de l'utilisateur actuel
    if etudiant_id is None:
        etudiant_id = current_user.id
    else:
        # Vérifier les permissions
        if current_user.role == UserRole.ETUDIANT and current_user.id != int(etudiant_id):
            return jsonify({'message': 'Vous ne pouvez consulter que vos propres réclamations'}), 403
        elif current_user.role == UserRole.ENSEIGNANT:
            return jsonify({'message': 'Accès non autorisé'}), 403
    
    # Vérifier si l'étudiant existe
    etudiant = User.query.get(etudiant_id)
    if not etudiant or etudiant.role != UserRole.ETUDIANT:
        return jsonify({'message': 'Étudiant non trouvé'}), 404
    
    reclamations = Reclamation.query.filter_by(etudiant_id=etudiant_id).all()
    result = []
    
    for reclamation in reclamations:
        note = Note.query.get(reclamation.note_id)
        module = Module.query.get(note.module_id) if note else None
        
        result.append({
            'id': reclamation.id,
            'description': reclamation.description,
            'date_creation': reclamation.date_creation.isoformat(),
            'date_traitement': reclamation.date_traitement.isoformat() if reclamation.date_traitement else None,
            'statut': reclamation.statut.value,
            'commentaire_enseignant': reclamation.commentaire_enseignant,
            'commentaire_admin': reclamation.commentaire_admin,
            'note': {
                'id': note.id,
                'module': module.nom if module else 'Module inconnu',
                'note_theorique': note.note_theorique,
                'note_pratique': note.note_pratique,
                'moyenne': note.moyenne
            } if note else None
        })
    
    return jsonify({'reclamations': result}), 200

# Obtenir les réclamations pour un enseignant
@token_required

# Obtenir les réclamations pour un enseignant
@token_required
def get_reclamations_by_enseignant(current_user):
    if current_user.role != UserRole.ENSEIGNANT:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    # Récupérer les modules enseignés par l'enseignant
    modules = Module.query.filter_by(enseignant_id=current_user.id).all()
    module_ids = [module.id for module in modules]
    
    # Récupérer les notes associées à ces modules
    notes = Note.query.filter(Note.module_id.in_(module_ids)).all()
    note_ids = [note.id for note in notes]
    
    # Récupérer les réclamations associées à ces notes
    reclamations = Reclamation.query.filter(Reclamation.note_id.in_(note_ids)).all()
    
    result = []
    for reclamation in reclamations:
        etudiant = User.query.get(reclamation.etudiant_id)
        note = Note.query.get(reclamation.note_id)
        module = Module.query.get(note.module_id) if note else None
        
        result.append({
            'id': reclamation.id,
            'description': reclamation.description,
            'date_creation': reclamation.date_creation.isoformat(),
            'date_traitement': reclamation.date_traitement.isoformat() if reclamation.date_traitement else None,
            'statut': reclamation.statut.value,
            'commentaire_enseignant': reclamation.commentaire_enseignant,
            'commentaire_admin': reclamation.commentaire_admin,
            'etudiant': {
                'id': etudiant.id,
                'nom': f"{etudiant.name} {etudiant.lastname}",
                'im': etudiant.im
            },
            'note': {
                'id': note.id,
                'module': module.nom if module else 'Module inconnu',
                'note_theorique': note.note_theorique,
                'note_pratique': note.note_pratique,
                'moyenne': note.moyenne
            } if note else None
        })
    
    return jsonify({'reclamations': result}), 200

# Traiter une réclamation par un enseignant
@token_required
def process_reclamation_by_enseignant(current_user, reclamation_id, data):
    if current_user.role != UserRole.ENSEIGNANT:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if 'commentaire' not in data or 'decision' not in data:
        return jsonify({'message': 'Données manquantes'}), 400
    
    if data['decision'] not in ['valider', 'rejeter']:
        return jsonify({'message': 'Décision invalide'}), 400
    
    reclamation = Reclamation.query.get_or_404(reclamation_id)
    
    # Vérifier si la réclamation est en attente
    if reclamation.statut != StatutReclamation.EN_ATTENTE:
        return jsonify({'message': 'Cette réclamation a déjà été traitée'}), 400
    
    # Vérifier si l'enseignant est responsable du module associé à la note
    note = Note.query.get(reclamation.note_id)
    if not note:
        return jsonify({'message': 'Note non trouvée'}), 404
    
    module = Module.query.get(note.module_id)
    if not module or module.enseignant_id != current_user.id:
        return jsonify({'message': 'Vous n\'êtes pas autorisé à traiter cette réclamation'}), 403
    
    # Mettre à jour la réclamation
    reclamation.commentaire_enseignant = data['commentaire']
    reclamation.date_traitement = datetime.datetime.utcnow()
    
    if data['decision'] == 'valider':
        reclamation.statut = StatutReclamation.VALIDEE_ENSEIGNANT
        
        # Si l'enseignant valide, mettre à jour la note si des nouvelles valeurs sont fournies
        if 'note_theorique' in data:
            note.note_theorique = data['note_theorique']
        
        if 'note_pratique' in data:
            note.note_pratique = data['note_pratique']
        
        # Recalculer la moyenne
        note.calculer_moyenne()
        note.date_modification = datetime.datetime.utcnow()
    else:
        reclamation.statut = StatutReclamation.REJETEE_ENSEIGNANT
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Réclamation traitée avec succès',
            'reclamation': {
                'id': reclamation.id,
                'statut': reclamation.statut.value,
                'commentaire_enseignant': reclamation.commentaire_enseignant,
                'date_traitement': reclamation.date_traitement.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors du traitement: {str(e)}'}), 500

# Traiter une réclamation par un admin
@token_required
def process_reclamation_by_admin(current_user, reclamation_id, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if 'commentaire' not in data or 'decision' not in data:
        return jsonify({'message': 'Données manquantes'}), 400
    
    if data['decision'] not in ['valider', 'rejeter']:
        return jsonify({'message': 'Décision invalide'}), 400
    
    reclamation = Reclamation.query.get_or_404(reclamation_id)
    
    # Vérifier si la réclamation peut être traitée par l'admin
    valid_statuses = [
        StatutReclamation.EN_ATTENTE,
        StatutReclamation.VALIDEE_ENSEIGNANT,
        StatutReclamation.REJETEE_ENSEIGNANT
    ]
    
    if reclamation.statut not in valid_statuses:
        return jsonify({'message': 'Cette réclamation ne peut pas être traitée'}), 400
    
    # Mettre à jour la réclamation
    reclamation.commentaire_admin = data['commentaire']
    reclamation.date_traitement = datetime.datetime.utcnow()
    
    note = Note.query.get(reclamation.note_id)
    if not note:
        return jsonify({'message': 'Note non trouvée'}), 404
    
    if data['decision'] == 'valider':
        reclamation.statut = StatutReclamation.VALIDEE_ADMIN
        
        # Si l'admin valide, mettre à jour la note si des nouvelles valeurs sont fournies
        if 'note_theorique' in data:
            note.note_theorique = data['note_theorique']
        
        if 'note_pratique' in data:
            note.note_pratique = data['note_pratique']
        
        # Recalculer la moyenne
        note.calculer_moyenne()
        note.date_modification = datetime.datetime.utcnow()
    else:
        reclamation.statut = StatutReclamation.REJETEE_ADMIN
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Réclamation traitée avec succès',
            'reclamation': {
                'id': reclamation.id,
                'statut': reclamation.statut.value,
                'commentaire_admin': reclamation.commentaire_admin,
                'date_traitement': reclamation.date_traitement.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors du traitement: {str(e)}'}), 500

# Obtenir une réclamation spécifique
@token_required
def get_reclamation(current_user, reclamation_id):
    reclamation = Reclamation.query.get_or_404(reclamation_id)
    
    # Vérifier les permissions
    if current_user.role == UserRole.ETUDIANT and reclamation.etudiant_id != current_user.id:
        return jsonify({'message': 'Vous n\'êtes pas autorisé à consulter cette réclamation'}), 403
    
    if current_user.role == UserRole.ENSEIGNANT:
        # Vérifier si l'enseignant est responsable du module associé à la note
        note = Note.query.get(reclamation.note_id)
        if not note:
            return jsonify({'message': 'Note non trouvée'}), 404
        
        module = Module.query.get(note.module_id)
        if not module or module.enseignant_id != current_user.id:
            return jsonify({'message': 'Vous n\'êtes pas autorisé à consulter cette réclamation'}), 403
    
    etudiant = User.query.get(reclamation.etudiant_id)
    note = Note.query.get(reclamation.note_id)
    module = Module.query.get(note.module_id) if note else None
    
    return jsonify({
        'id': reclamation.id,
        'description': reclamation.description,
        'date_creation': reclamation.date_creation.isoformat(),
        'date_traitement': reclamation.date_traitement.isoformat() if reclamation.date_traitement else None,
        'statut': reclamation.statut.value,
        'commentaire_enseignant': reclamation.commentaire_enseignant,
        'commentaire_admin': reclamation.commentaire_admin,
        'etudiant': {
            'id': etudiant.id,
            'nom': f"{etudiant.name} {etudiant.lastname}",
            'im': etudiant.im
        },
        'note': {
            'id': note.id,
            'module': module.nom if module else 'Module inconnu',
            'note_theorique': note.note_theorique,
            'note_pratique': note.note_pratique,
            'moyenne': note.moyenne
        } if note else None
    }), 200
