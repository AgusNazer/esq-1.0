from flask import Blueprint, jsonify, request

auth = Blueprint('auth', __name__)

base_url = '/src/auth/'

@auth.route(base_url + 'issue_token', methods=['POST'])
def issue_token():
    try:
        user_data = request.get_json()
    except Exception as e:
        return jsonify({'result': False, 'response': f'Error en la solicitud: {e}'}), 400