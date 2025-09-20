"""
检查数据库中的用户信息
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import create_app
from models import db, User, Department, Role

def check_database():
    """检查数据库中的用户信息"""
    app = create_app()
    
    with app.app_context():
        # 检查用户
        users = User.query.all()
        print("用户列表:")
        for user in users:
            print(f"  ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 角色: {user.role}")
        
        # 检查部门
        departments = Department.query.all()
        print("\n部门列表:")
        for dept in departments:
            print(f"  ID: {dept.id}, 名称: {dept.name}, 描述: {dept.description}")
        
        # 检查角色
        roles = Role.query.all()
        print("\n角色列表:")
        for role in roles:
            print(f"  ID: {role.id}, 名称: {role.name}, 描述: {role.description}")

if __name__ == '__main__':
    check_database()