# src/auth/auth.py
from flask import Blueprint, jsonify, request, make_response, render_template, session, session as flask_session, current_app, redirect, url_for
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta
from functools import wraps
from src.models.user import User
#Alchemy
from config_db import SessionLocal  # Importa la sesión de SQLAlchemy

#hash security
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)

# Middleware para verificar el token
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 403
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Alert': 'Invalid Token!'}), 403
        return func(*args, **kwargs)
    return decorated

# Función para verificar la existencia de un usuario
def get_user_by_username_or_email(username, email):
    session = SessionLocal()
    try:
        return session.query(User).filter((User.username == username) | (User.email == email)).first()
    finally:
        session.close()

# Función para guardar un usuario en la base de datos
def save_user(username, email, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    session = SessionLocal()
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise ValueError("Username or email already exists")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Devolver el template 'login.html' que contiene ambos formularios
        return render_template('login.html')

    elif request.method == 'POST':
        # Procesar el formulario de registro
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Nombre de usuario, correo electrónico y contraseña son obligatorios'}), 400

        try:
            # Verificar usuario existente
            existing_user = get_user_by_username_or_email(username, email)
            if existing_user:
                return jsonify({'message': 'El usuario o correo electrónico ya existe'}), 400

            user = save_user(username, email, password)
            return jsonify({'message': 'Usuario registrado exitosamente', 'username': user.username}), 201
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': 'Error al registrar el usuario', 'detalles': str(e)}), 500

    else:
        return jsonify({'error': 'Método no permitido'}), 405

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        session = SessionLocal()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    token = jwt.encode({
                        'user': user.username,
                        'exp': datetime.utcnow() + timedelta(seconds=120)
                    }, current_app.config['SECRET_KEY'], algorithm="HS256")
                    flask_session['token'] = token
                    return jsonify({'token': token}), 200
                else:
                    return jsonify({'error': 'Incorrect username or password'}), 403
            else:
                return jsonify({'error': 'User not found, please register first'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to authenticate', 'details': str(e)}), 500
        finally:
            session.close()
    else:
        return render_template('login.html')
    
@auth.route('/logout', methods=['POST'])
def logout():
    flask_session.pop('token', None)
    return redirect(url_for('auth.login'))  # Redirige a la ruta de login

#decorador para verificar tokens

def login_decoration(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token')
        if token is None:
            return redirect(url_for('auth.login', next = request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/public')
def public():
    return 'For public'

@auth.route('/auth')
@token_required
def auth_route():
    return 'JWT is verified. Welcome to your dashboard!'
