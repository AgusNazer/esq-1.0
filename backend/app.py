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
from src.views.home import home_admin

load_dotenv()

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(home_admin, url_prefix='/home')


Base.metadata.create_all(bind=engine)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return 'Hello, World'
# sssss
if __name__ == '__main__':
    app.run(debug=True)