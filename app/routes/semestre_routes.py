from flask import Blueprint, request
from app.controllers.semestre_controller import (
    create_semestre, get_all_semestres, get_semestre,
    update_semestre, delete_semestre
)

semestre_routes = Blueprint('semestre_routes', __name__)

@semestre_routes.route('/', methods=['POST'])
def add_semestre():
    data = request.get_json()
    return create_semestre(data)

@semestre_routes.route('/', methods=['GET'])
def list_semestres():
    return get_all_semestres()

@semestre_routes.route('/<int:semestre_id>', methods=['GET'])
def view_semestre(semestre_id):
    return get_semestre(semestre_id)

@semestre_routes.route('/<int:semestre_id>', methods=['PUT'])
def edit_semestre(semestre_id):
    data = request.get_json()
    return update_semestre(semestre_id, data)

@semestre_routes.route('/<int:semestre_id>', methods=['DELETE'])
def remove_semestre(semestre_id):
    return delete_semestre(semestre_id)
