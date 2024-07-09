# src/auth/auth.py
from flask import Blueprint, jsonify, request, make_response, render_template, session, current_app, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth = Blueprint('auth', __name__)

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

@auth.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm="Authentication Failed!"'})
         
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
