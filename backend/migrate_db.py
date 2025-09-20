"""
数据库迁移脚本
添加部门和角色相关字段到用户表
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import create_app
from models import db

def migrate_database():
    """迁移数据库表结构"""
    app = create_app()
    
    with app.app_context():
        # 使用 SQLAlchemy 的反射功能来获取现有表结构
        from sqlalchemy import text
        
        try:
            # 检查是否已存在 department_id 列
            result = db.session.execute(text("PRAGMA table_info(user)")).fetchall()
            columns = [row[1] for row in result]
            
            # 添加 department_id 列（如果不存在）
            if 'department_id' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN department_id INTEGER"))
                print("已添加 department_id 列")
            
            # 添加 role_id 列（如果不存在）
            if 'role_id' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN role_id INTEGER"))
                print("已添加 role_id 列")
            
            # 添加 data_scope 列（如果不存在）
            if 'data_scope' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN data_scope VARCHAR(20) DEFAULT 'own'"))
                print("已添加 data_scope 列")
            
            # 提交更改
            db.session.commit()
            print("数据库迁移完成!")
            
        except Exception as e:
            print(f"迁移过程中出现错误: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database()