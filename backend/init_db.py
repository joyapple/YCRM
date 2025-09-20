"""
初始化数据库脚本
创建默认管理员用户
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import create_app
from models import db, User

def init_database():
    """初始化数据库并创建默认管理员用户"""
    app = create_app()
    
    with app.app_context():
        # 检查是否已存在管理员用户
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            # 创建默认管理员用户
            admin = User(
                username='admin',
                email='admin@ycrm.com',
                role='admin'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            print("默认管理员用户创建成功!")
            print("用户名: admin")
            print("密码: admin123")
        else:
            print("管理员用户已存在，无需创建")

if __name__ == '__main__':
    init_database()