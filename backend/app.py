from flask import Flask
from src.routes.user import users
from config_db import engine
from src.models.user import Base
from flask import Flask, Blueprint, jsonify, request, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from src.auth.auth import auth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(auth, url_prefix='/auth')


Base.metadata.create_all(bind=engine)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request/args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing'})
#         try:
#             payload = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'Alert': 'Invalid Token!'})
#     return decorated

# #home
# @app.route('/home')
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return 'Logged in currently!'

# @app.route('/login', methods=['POST'])
# def login():
#     if request.form['username'] and request.form['password'] == '123456':
#         session['logged_in'] = True
#         token = jwt.encode({
#             'user': request.form['username'],
#             'expiration': str(datetime.utcnow() + timedelta(seconds=120))
#         }, app.config['SECRET_KEY'], algorithm="HS256")
#         return jsonify({'token': token})
#     else:
#         return make_response('Unable to verify', 403, {'WWW.Authenticate' : 'Basic realm: "Authentication Failed!'})


# @app.route('/public')
# def public():
#     return 'For public'

# #auth
# @app.route('/auth')
# @token_required
# def auth():
#     return 'JWT is verified. Welcome to your dashboard!'


@app.route('/')
def hello_world():
    return 'Hello, World'
# sssss
if __name__ == '__main__':
    app.run(debug=True)