from flask import Blueprint, request
from app.controllers.reclamation_controller import (
    create_reclamation, get_all_reclamations, get_reclamations_by_etudiant,
    get_reclamations_by_enseignant, process_reclamation_by_enseignant,
    process_reclamation_by_admin, get_reclamation
)

reclamation_routes = Blueprint('reclamation_routes', __name__)

@reclamation_routes.route('/', methods=['POST'])
def add_reclamation():
    data = request.get_json()
    return create_reclamation(data)

@reclamation_routes.route('/', methods=['GET'])
def list_reclamations():
    return get_all_reclamations()

@reclamation_routes.route('/<int:reclamation_id>', methods=['GET'])
def view_reclamation(reclamation_id):
    return get_reclamation(reclamation_id)

@reclamation_routes.route('/etudiant/', methods=['GET'])
def list_reclamations_by_current_etudiant():
    return get_reclamations_by_etudiant()

@reclamation_routes.route('/etudiant/<int:etudiant_id>', methods=['GET'])
def list_reclamations_by_etudiant(etudiant_id):
    return get_reclamations_by_etudiant(etudiant_id)

@reclamation_routes.route('/enseignant/', methods=['GET'])
def list_reclamations_by_enseignant():
    return get_reclamations_by_enseignant()

@reclamation_routes.route('/enseignant/process/<int:reclamation_id>', methods=['PUT'])
def process_by_enseignant(reclamation_id):
    data = request.get_json()
    return process_reclamation_by_enseignant(reclamation_id, data)

@reclamation_routes.route('/admin/process/<int:reclamation_id>', methods=['PUT'])
def process_by_admin(reclamation_id):
    data = request.get_json()
    return process_reclamation_by_admin(reclamation_id, data)
