from flask import Blueprint, request
from app.controllers.classe_controller import (
    create_classe, get_all_classes, get_classe,
    update_classe, delete_classe
)

classe_routes = Blueprint('classe_routes', __name__)

@classe_routes.route('/', methods=['POST'])
def add_classe():
    data = request.get_json()
    return create_classe(data)

@classe_routes.route('/', methods=['GET'])
def list_classes():
    return get_all_classes()

@classe_routes.route('/<int:classe_id>', methods=['GET'])
def view_classe(classe_id):
    return get_classe(classe_id)

@classe_routes.route('/<int:classe_id>', methods=['PUT'])
def edit_classe(classe_id):
    data = request.get_json()
    return update_classe(classe_id, data)

@classe_routes.route('/<int:classe_id>', methods=['DELETE'])
def remove_classe(classe_id):
    return delete_classe(classe_id)
