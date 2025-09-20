from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化迁移工具
    migrate = Migrate(app, db)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Migration environment initialized successfully!")