import os
import datetime
from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from database import Session
from User import User
from middleware import token_required

auth_bp = Blueprint('auth', __name__)
secret_key = os.environ.get('SECRET_KEY', 'secret')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    session = Session()
    
    if session.query(User).filter_by(username=data['username']).first():
        session.close()
        return jsonify({"message": "User already exists"}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'], 
        password_hash=hashed_pw, 
        role=data.get('role', 'user')
    )
    
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    session = Session()
    user = session.query(User).filter_by(username=data['username']).first()
    session.close()

    if user and check_password_hash(user.password_hash, data['password']):
        token_payload = {
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")
        return jsonify({"token": token})
    
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        'id': user.id, 
        'username': user.username, 
        'role': user.role
    })