from flask import Flask
from models import db, Opportunity, Order, User
from config import Config
import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def migrate_tables():
    """迁移数据库表结构，添加user_id字段"""
    app = create_app()
    
    with app.app_context():
        # 添加Opportunity表的user_id字段
        try:
            # 检查字段是否已存在
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('opportunity')
            column_names = [column['name'] for column in columns]
            
            if 'user_id' not in column_names:
                # 由于SQLite不支持直接添加外键约束，我们使用Alembic风格的迁移
                # 这里我们采用一种简单的方法：添加字段并设置默认值
                db.engine.execute('ALTER TABLE opportunity ADD COLUMN user_id INTEGER')
                print("已向opportunity表添加user_id字段")
            else:
                print("opportunity表已存在user_id字段")
        except Exception as e:
            print(f"向opportunity表添加user_id字段时出错: {e}")
        
        # 添加Order表的user_id字段
        try:
            # 检查字段是否已存在
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('order')
            column_names = [column['name'] for column in columns]
            
            if 'user_id' not in column_names:
                # 由于SQLite不支持直接添加外键约束，我们使用Alembic风格的迁移
                db.engine.execute('ALTER TABLE "order" ADD COLUMN user_id INTEGER')
                print("已向order表添加user_id字段")
            else:
                print("order表已存在user_id字段")
        except Exception as e:
            print(f"向order表添加user_id字段时出错: {e}")
        
        # 为现有的商机和订单记录设置默认用户ID（设置为第一个管理员用户）
        try:
            admin_user = User.query.filter_by(role='admin').first()
            if admin_user:
                # 更新商机表中的user_id字段
                opportunities = Opportunity.query.filter(Opportunity.user_id.is_(None)).all()
                for opportunity in opportunities:
                    opportunity.user_id = admin_user.id
                
                # 更新订单表中的user_id字段
                orders = Order.query.filter(Order.user_id.is_(None)).all()
                for order in orders:
                    order.user_id = admin_user.id
                
                db.session.commit()
                print(f"已为 {len(opportunities)} 个商机和 {len(orders)} 个订单设置默认用户ID")
            else:
                print("未找到管理员用户，无法设置默认用户ID")
        except Exception as e:
            print(f"设置默认用户ID时出错: {e}")

if __name__ == '__main__':
    migrate_tables()
    print("数据库迁移完成!")