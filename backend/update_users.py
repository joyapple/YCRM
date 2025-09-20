"""
更新现有用户信息
分配默认部门和角色
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import create_app
from models import db, User, Department, Role

def update_users():
    """更新现有用户信息"""
    app = create_app()
    
    with app.app_context():
        # 获取默认部门和角色
        sales_dept = Department.query.filter_by(name="销售部").first()
        admin_role = Role.query.filter_by(name="系统管理员").first()
        sales_manager_role = Role.query.filter_by(name="销售经理").first()
        
        # 更新管理员用户
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.department_id = sales_dept.id if sales_dept else None
            admin_user.role_id = admin_role.id if admin_role else None
            admin_user.data_scope = 'all'
            print(f"已更新管理员用户: {admin_user.username}")
        
        # 更新 joyapple 用户
        joyapple_user = User.query.filter_by(username='joyapple').first()
        if joyapple_user:
            joyapple_user.department_id = sales_dept.id if sales_dept else None
            joyapple_user.role_id = sales_manager_role.id if sales_manager_role else None
            joyapple_user.data_scope = 'department'
            print(f"已更新用户: {joyapple_user.username}")
        
        # 提交更改
        db.session.commit()
        print("用户信息更新完成!")

if __name__ == '__main__':
    update_users()