# src/auth/auth.py
from flask import Blueprint, jsonify, request, make_response, render_template, session, current_app, redirect, url_for
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

@auth.route('/register', methods=['POST'])
def register():
    # data = request.json
    # username = data.get('username')
    # email = data.get('email')
    # password = data.get('password')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
        
    
    try:
        #checkear usuario existente
        existing_user = get_user_by_username_or_email(username, email)
        if existing_user:
            return jsonify({'message': 'User or email already exists'}), 400
        
        user = save_user(username, email, password)
        return jsonify({'message': 'User registered successfully', 'username': user.username, 'password':user.password}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to register user', 'details': str(e)}), 500
    

@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Buscar al usuario por nombre de usuario
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            token = jwt.encode({
                'user': user.username,
                'exp': datetime.utcnow() + timedelta(seconds=120)  # Expira en 2 minutos
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            session.close()
            return jsonify({'token': token}), 200
        else:
            session.close()
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm="Authentication Failed!"'})
    except Exception as e:
        session.close()
        return jsonify({'error': 'Failed to authenticate', 'details': str(e)}), 500

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    # return jsonify({'message': 'Successfully logged out'}), 200return redirect(url_for('auth.home'))

    return redirect(url_for('auth.home'))


@auth.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'

@auth.route('/public')
def public():
    return 'For public'

@auth.route('/auth')
@token_required
def auth_route():
    return 'JWT is verified. Welcome to your dashboard!'
