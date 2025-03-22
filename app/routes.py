from flask import Blueprint, request, jsonify
from app.controllers import ajouter_etudiant, obtenir_tous_les_etudiants, obtenir_etudiant_par_id, mettre_a_jour_etudiant, supprimer_etudiant

main = Blueprint('main', __name__)

# Ajouter un étudiant
@main.route('/eleves', methods=['POST'])
def creer_eleve():
    data = request.json
    nouvel_eleve = ajouter_etudiant(data['nom'], data['note'])
    return jsonify(nouvel_eleve.to_dict()), 201

# Lire tous les étudiants
@main.route('/eleves', methods=['GET'])
def lire_tous_les_eleves():
    eleves = obtenir_tous_les_etudiants()
    return jsonify([eleve.to_dict() for eleve in eleves])

# Lire un étudiant spécifique
@main.route('/eleves/<int:eleve_id>', methods=['GET'])
def lire_un_eleve(eleve_id):
    eleve = obtenir_etudiant_par_id(eleve_id)
    if not eleve:
        return jsonify({'message': 'Élève non trouvé'}), 404
    return jsonify(eleve.to_dict())

# Mettre à jour un étudiant
@main.route('/eleves/<int:eleve_id>', methods=['PUT'])
def maj_eleve(eleve_id):
    data = request.json
    eleve = mettre_a_jour_etudiant(eleve_id, data.get('nom'), data.get('note'))
    if not eleve:
        return jsonify({'message': 'Élève non trouvé'}), 404
    return jsonify(eleve.to_dict())

# Supprimer un étudiant
@main.route('/eleves/<int:eleve_id>', methods=['DELETE'])
def supprimer_eleve(eleve_id):
    eleve = supprimer_etudiant(eleve_id)
    if not eleve:
        return jsonify({'message': 'Élève non trouvé'}), 404
    return jsonify({'message': 'Élève supprimé avec succès'})
