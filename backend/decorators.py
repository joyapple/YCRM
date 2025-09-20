from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User, db

def admin_required(f):
    """
    管理员权限检查装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'status': 'error'}), 404
            
        if not user.is_admin():
            return jsonify({'message': 'Admin permission required', 'status': 'error'}), 403
            
        return f(*args, **kwargs)
    
    return decorated_function

def permission_required(required_role):
    """
    指定角色权限检查装饰器
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'message': 'User not found', 'status': 'error'}), 404
                
            if user.role != required_role and not user.is_admin():
                return jsonify({'message': f'{required_role} permission required', 'status': 'error'}), 403
                
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator