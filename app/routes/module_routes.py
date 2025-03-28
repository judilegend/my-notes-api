from flask import Blueprint, request
from app.controllers.module_controller import (
    create_module, get_all_modules, get_module,
    update_module, delete_module, get_modules_by_enseignant
)

module_routes = Blueprint('module_routes', __name__)

@module_routes.route('/', methods=['POST'])
def add_module():
    data = request.get_json()
    return create_module(data)

@module_routes.route('/', methods=['GET'])
def list_modules():
    return get_all_modules()

@module_routes.route('/<int:module_id>', methods=['GET'])
def view_module(module_id):
    return get_module(module_id)

@module_routes.route('/<int:module_id>', methods=['PUT'])
def edit_module(module_id):
    data = request.get_json()
    return update_module(module_id, data)

@module_routes.route('/<int:module_id>', methods=['DELETE'])
def remove_module(module_id):
    return delete_module(module_id)

@module_routes.route('/enseignant/', methods=['GET'])
def list_modules_by_current_enseignant():
    return get_modules_by_enseignant()

@module_routes.route('/enseignant/<int:enseignant_id>', methods=['GET'])
def list_modules_by_enseignant(enseignant_id):
    return get_modules_by_enseignant(enseignant_id)
