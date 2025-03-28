from app import db
from app.models.classe import Classe
from app.models.user import User, UserRole
from app.controllers.user_controller import token_required
from flask import jsonify, request

# Créer une nouvelle classe (Admin uniquement)
@token_required
def create_classe(current_user, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if not all(key in data for key in ['nom', 'niveau']):
        return jsonify({'message': 'Données manquantes'}), 400
    
    new_classe = Classe(
        nom=data['nom'],
        niveau=data['niveau']
    )
    
    try:
        db.session.add(new_classe)
        db.session.commit()
        return jsonify({
            'message': 'Classe créée avec succès',
            'classe': {
                'id': new_classe.id,
                'nom': new_classe.nom,
                'niveau': new_classe.niveau
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la création: {str(e)}'}), 500

# Obtenir toutes les classes
@token_required
def get_all_classes(current_user):
    classes = Classe.query.all()
    result = []
    
    for classe in classes:
        result.append({
            'id': classe.id,
            'nom': classe.nom,
            'niveau': classe.niveau
        })
    
    return jsonify({'classes': result}), 200

# Obtenir une classe spécifique
@token_required
def get_classe(current_user, classe_id):
    classe = Classe.query.get_or_404(classe_id)
    
    return jsonify({
        'id': classe.id,
        'nom': classe.nom,
        'niveau': classe.niveau
    }), 200

# Mettre à jour une classe (Admin uniquement)
@token_required
def update_classe(current_user, classe_id, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    classe = Classe.query.get_or_404(classe_id)
    
    if 'nom' in data:
        classe.nom = data['nom']
    if 'niveau' in data:
        classe.niveau = data['niveau']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Classe mise à jour avec succès',
            'classe': {
                'id': classe.id,
                'nom': classe.nom,
                'niveau': classe.niveau
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la mise à jour: {str(e)}'}), 500

# Supprimer une classe (Admin uniquement)
@token_required
def delete_classe(current_user, classe_id):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    classe = Classe.query.get_or_404(classe_id)
    
    try:
        db.session.delete(classe)
        db.session.commit()
        return jsonify({'message': 'Classe supprimée avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la suppression: {str(e)}'}), 500
