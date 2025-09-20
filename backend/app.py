from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化迁移工具
    migrate = Migrate(app, db)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 添加CORS支持
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(api, url_prefix='/api')
    
    # 创建表
    with app.app_context():
        db.create_all()
    
    # 添加JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'message': 'Token has expired', 'status': 'error'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'Invalid token', 'status': 'error'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'message': 'Missing token', 'status': 'error'}), 401
    
    @app.route('/')
    def hello():
        return jsonify({"message": "Welcome to YCRM API", "status": "success"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)