from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.models.user import User
from config_db import SessionLocal

users = Blueprint('users', __name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users.route('/get_all_users', methods=['GET'])
def get_all_users():
    db = next(get_db())
    users = db.query(User).all()
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list), 200
    
 

@users.route('/create_user', methods=['POST'])
def create_user():
    if request.headers['Content-Type'] != 'application/json':
       return jsonify({"error": "Unsupported Media Type"}), 415
    
    data = request.get_json()
   
    # Validar datos de entrada
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']  # argegar JWT
    
    db = next(get_db())
    try:
        new_user = User(username=username, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500
