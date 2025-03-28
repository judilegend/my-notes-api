from app import db
from app.models.module import Module
from app.models.classe import Classe
from app.models.semestre import Semestre
from app.models.user import User, UserRole
from app.controllers.user_controller import token_required
from flask import jsonify, request

# Créer un nouveau module (Admin uniquement)
@token_required
def create_module(current_user, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    if not all(key in data for key in ['nom', 'code', 'credits', 'semestre_id']):
        return jsonify({'message': 'Données manquantes'}), 400
    
    # Vérifier si le semestre existe
    semestre = Semestre.query.get(data['semestre_id'])
    if not semestre:
        return jsonify({'message': 'Semestre non trouvé'}), 404
    
    # Vérifier si l'enseignant existe (si fourni)
    enseignant_id = data.get('enseignant_id')
    if enseignant_id:
        enseignant = User.query.get(enseignant_id)
        if not enseignant or enseignant.role != UserRole.ENSEIGNANT:
            return jsonify({'message': 'Enseignant non valide'}), 400
    
    # Vérifier si le code du module est unique
    if Module.query.filter_by(code=data['code']).first():
        return jsonify({'message': 'Ce code de module existe déjà'}), 400
    
    new_module = Module(
        nom=data['nom'],
        code=data['code'],
        credits=data['credits'],
        semestre_id=data['semestre_id'],
        enseignant_id=enseignant_id
    )
    
    # Associer les classes si fournies
    if 'classe_ids' in data and isinstance(data['classe_ids'], list):
        for classe_id in data['classe_ids']:
            classe = Classe.query.get(classe_id)
            if classe:
                new_module.classes.append(classe)
    
    try:
        db.session.add(new_module)
        db.session.commit()
        
        # Préparer les données des classes pour la réponse
        classes = []
        for classe in new_module.classes:
            classes.append({
                'id': classe.id,
                'nom': classe.nom,
                'niveau': classe.niveau
            })
        
        return jsonify({
            'message': 'Module créé avec succès',
            'module': {
                'id': new_module.id,
                'nom': new_module.nom,
                'code': new_module.code,
                'credits': new_module.credits,
                'semestre_id': new_module.semestre_id,
                'enseignant_id': new_module.enseignant_id,
                'classes': classes
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la création: {str(e)}'}), 500

# Obtenir tous les modules
@token_required
def get_all_modules(current_user):
    modules = Module.query.all()
    result = []
    
    for module in modules:
        # Préparer les données des classes pour la réponse
        classes = []
        for classe in module.classes:
            classes.append({
                'id': classe.id,
                'nom': classe.nom,
                'niveau': classe.niveau
            })
        
        result.append({
            'id': module.id,
            'nom': module.nom,
            'code': module.code,
            'credits': module.credits,
            'semestre_id': module.semestre_id,
            'enseignant_id': module.enseignant_id,
            'classes': classes
        })
    
    return jsonify({'modules': result}), 200

# Obtenir un module spécifique
@token_required
def get_module(current_user, module_id):
    module = Module.query.get_or_404(module_id)
    
    # Préparer les données des classes pour la réponse
    classes = []
    for classe in module.classes:
        classes.append({
            'id': classe.id,
            'nom': classe.nom,
            'niveau': classe.niveau
        })
    
    return jsonify({
        'id': module.id,
        'nom': module.nom,
        'code': module.code,
        'credits': module.credits,
        'semestre_id': module.semestre_id,
        'enseignant_id': module.enseignant_id,
        'classes': classes
    }), 200

# Mettre à jour un module (Admin uniquement)
@token_required
def update_module(current_user, module_id, data):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    module = Module.query.get_or_404(module_id)
    
    if 'nom' in data:
        module.nom = data['nom']
    
    if 'code' in data:
        # Vérifier si le nouveau code est unique
        existing_module = Module.query.filter_by(code=data['code']).first()
        if existing_module and existing_module.id != module_id:
            return jsonify({'message': 'Ce code de module existe déjà'}), 400
        module.code = data['code']
    
    if 'credits' in data:
        module.credits = data['credits']
    
    if 'semestre_id' in data:
        # Vérifier si le semestre existe
        semestre = Semestre.query.get(data['semestre_id'])
        if not semestre:
            return jsonify({'message': 'Semestre non trouvé'}), 404
        module.semestre_id = data['semestre_id']
    
    if 'enseignant_id' in data:
        # Vérifier si l'enseignant existe
        if data['enseignant_id'] is not None:
            enseignant = User.query.get(data['enseignant_id'])
            if not enseignant or enseignant.role != UserRole.ENSEIGNANT:
                return jsonify({'message': 'Enseignant non valide'}), 400
        module.enseignant_id = data['enseignant_id']
    
    # Mettre à jour les classes associées si fournies
    if 'classe_ids' in data and isinstance(data['classe_ids'], list):
        # Supprimer toutes les associations existantes
        module.classes = []
        
        # Ajouter les nouvelles associations
        for classe_id in data['classe_ids']:
            classe = Classe.query.get(classe_id)
            if classe:
                module.classes.append(classe)
    
    try:
        db.session.commit()
        
        # Préparer les données des classes pour la réponse
        classes = []
        for classe in module.classes:
            classes.append({
                'id': classe.id,
                'nom': classe.nom,
                'niveau': classe.niveau
            })
        
        return jsonify({
            'message': 'Module mis à jour avec succès',
            'module': {
                'id': module.id,
                'nom': module.nom,
                'code': module.code,
                'credits': module.credits,
                'semestre_id': module.semestre_id,
                'enseignant_id': module.enseignant_id,
                'classes': classes
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la mise à jour: {str(e)}'}), 500

# Supprimer un module (Admin uniquement)
@token_required
def delete_module(current_user, module_id):
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    module = Module.query.get_or_404(module_id)
    
    try:
        db.session.delete(module)
        db.session.commit()
        return jsonify({'message': 'Module supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la suppression: {str(e)}'}), 500

# Obtenir les modules enseignés par un enseignant
@token_required
def get_modules_by_enseignant(current_user, enseignant_id=None):
    # Si l'enseignant_id n'est pas fourni, utiliser l'ID de l'utilisateur actuel
    if enseignant_id is None:
        if current_user.role != UserRole.ENSEIGNANT:
            return jsonify({'message': 'Accès non autorisé'}), 403
        enseignant_id = current_user.id
    else:
        # Vérifier si l'utilisateur actuel est admin ou l'enseignant lui-même
        if current_user.role != UserRole.ADMIN and current_user.id != int(enseignant_id):
            return jsonify({'message': 'Accès non autorisé'}), 403
    
    # Vérifier si l'enseignant existe
    enseignant = User.query.get(enseignant_id)
    if not enseignant or enseignant.role != UserRole.ENSEIGNANT:
        return jsonify({'message': 'Enseignant non trouvé'}), 404
    
    modules = Module.query.filter_by(enseignant_id=enseignant_id).all()
    result = []
    
    for module in modules:
        # Préparer les données des classes pour la réponse
        classes = []
        for classe in module.classes:
            classes.append({
                'id': classe.id,
                'nom': classe.nom,
                'niveau': classe.niveau
            })
        
        result.append({
            'id': module.id,
            'nom': module.nom,
            'code': module.code,
            'credits': module.credits,
            'semestre_id': module.semestre_id,
            'classes': classes
        })
    
    return jsonify({'modules': result}), 200
