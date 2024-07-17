from flask import Blueprint, render_template, session, redirect, url_for, request, make_response
from functools import wraps
from src.models.user import User

home_admin = Blueprint('home', __name__)

# Decorador (middleware) para proteger ruta
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token')
        if token is None:
            return redirect(url_for('auth.login', next=request.url))
        response = make_response(f(*args, **kwargs))
        #No guardar cache, principalmente para que el for.. del usuario nopueda volver atras luego del logout y ver contenido
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return decorated_function

@home_admin.route('/', methods=['GET'])
@login_required
def home():
    return render_template('index.html')
