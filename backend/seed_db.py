"""
初始化数据库种子数据
创建默认部门和角色
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import create_app
from models import db, Department, Role

def seed_database():
    """初始化数据库种子数据"""
    app = create_app()
    
    with app.app_context():
        # 创建默认部门
        departments_data = [
            {"name": "销售部", "description": "负责客户开发和销售业务"},
            {"name": "市场部", "description": "负责市场推广和品牌建设"},
            {"name": "技术部", "description": "负责产品开发和技术支持"},
            {"name": "人事部", "description": "负责人力资源管理"},
            {"name": "财务部", "description": "负责财务管理"}
        ]
        
        for dept_data in departments_data:
            # 检查部门是否已存在
            existing_dept = Department.query.filter_by(name=dept_data["name"]).first()
            if not existing_dept:
                dept = Department(**dept_data)
                db.session.add(dept)
                print(f"已创建部门: {dept_data['name']}")
        
        # 创建默认角色
        roles_data = [
            {"name": "系统管理员", "description": "拥有系统全部权限", "permissions": '["admin"]'},
            {"name": "销售经理", "description": "负责销售团队管理", "permissions": '["view_customer", "create_customer", "edit_customer", "delete_customer", "view_followup", "create_followup", "edit_followup", "delete_followup", "view_opportunity", "create_opportunity", "edit_opportunity", "delete_opportunity", "view_order", "create_order", "edit_order", "delete_order"]'},
            {"name": "销售专员", "description": "负责客户开发和维护", "permissions": '["view_customer", "create_customer", "edit_customer", "view_followup", "create_followup", "edit_followup", "view_opportunity", "create_opportunity", "edit_opportunity", "view_order", "create_order", "edit_order"]'},
            {"name": "市场专员", "description": "负责市场推广活动", "permissions": '["view_customer", "view_followup", "view_opportunity"]'}
        ]
        
        for role_data in roles_data:
            # 检查角色是否已存在
            existing_role = Role.query.filter_by(name=role_data["name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.session.add(role)
                print(f"已创建角色: {role_data['name']}")
        
        # 提交更改
        db.session.commit()
        print("数据库种子数据初始化完成!")

if __name__ == '__main__':
    seed_database()