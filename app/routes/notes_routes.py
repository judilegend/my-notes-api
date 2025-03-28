@note_routes.route('/', methods=['POST'])
def create_note():
    data = request.get_json()
    return add_note(data)

@note_routes.route('/<int:note_id>', methods=['PUT'])
def modify_note(note_id):
    data = request.get_json()
    return update_note(note_id, data)

@note_routes.route('/', methods=['GET'])
def list_notes():
    return get_all_notes()

@note_routes.route('/etudiant/', methods=['GET'])
def list_notes_by_current_etudiant():
    return get_notes_by_etudiant()

@note_routes.route('/etudiant/<int:etudiant_id>', methods=['GET'])
def list_notes_by_etudiant(etudiant_id):
    return get_notes_by_etudiant(etudiant_id)

@note_routes.route('/module/<int:module_id>', methods=['GET'])
def list_notes_by_module(module_id):
    return get_notes_by_module(module_id)

@note_routes.route('/<int:note_id>', methods=['DELETE'])
def remove_note(note_id):
    return delete_note(note_id)
