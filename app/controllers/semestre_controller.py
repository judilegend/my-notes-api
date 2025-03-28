from app import db
from app.models.semestre import Semestre, SemestreType
from app.models.user import UserRole
from app.controllers.user_controller import token_required
from flask import jsonify, request

# Créer un nouveau semestre (Admin uniquement)
@token_required
def create_semestre(current_user, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if not all(key in data for key in ['type', 'annee_academique']):
        return jsonify({'message': 'Données manquantes'}), 400
    
    if data['type'] not in [s.name for s in SemestreType]:
        return jsonify({'message': 'Type de semestre invalide'}), 400
    
    new_semestre = Semestre(
        type=SemestreType[data['type']],
        annee_academique=data['annee_academique']
    )
    
    try:
        db.session.add(new_semestre)
        db.session.commit()
        return jsonify({
            'message': 'Semestre créé avec succès',
            'semestre': {
                'id': new_semestre.id,
                'type': new_semestre.type.value,
                'annee_academique': new_semestre.annee_academique
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la création: {str(e)}'}), 500

# Obtenir tous les semestres
@token_required
def get_all_semestres(current_user):
    semestres = Semestre.query.all()
    result = []
    
    for semestre in semestres:
        result.append({
            'id': semestre.id,
            'type': semestre.type.value,
            'annee_academique': semestre.annee_academique
        })
    
    return jsonify({'semestres': result}), 200

# Obtenir un semestre spécifique
@token_required
def get_semestre(current_user, semestre_id):
    semestre = Semestre.query.get_or_404(semestre_id)
    
    return jsonify({
        'id': semestre.id,
        'type': semestre.type.value,
        'annee_academique': semestre.annee_academique
    }), 200

# Mettre à jour un semestre (Admin uniquement)
@token_required
def update_semestre(current_user, semestre_id, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    semestre = Semestre.query.get_or_404(semestre_id)
    
    if 'type' in data:
        if data['type'] not in [s.name for s in SemestreType]:
            return jsonify({'message': 'Type de semestre invalide'}), 400
        semestre.type = SemestreType[data['type']]
    
    if 'annee_academique' in data:
        semestre.annee_academique = data['annee_academique']
    try:
        db.session.commit()
        return jsonify({
            'message': 'Semestre mis à jour avec succès',
            'semestre': {
                'id': semestre.id,
                'type': semestre.type.value,
                'annee_academique': semestre.annee_academique
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la mise à jour: {str(e)}'}), 500

# Supprimer un semestre (Admin uniquement)
@token_required
def delete_semestre(current_user, semestre_id):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    semestre = Semestre.query.get_or_404(semestre_id)
    
    try:
        db.session.delete(semestre)
        db.session.commit()
        return jsonify({'message': 'Semestre supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la suppression: {str(e)}'}), 500
