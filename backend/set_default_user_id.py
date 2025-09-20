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

def set_default_user_id():
    """为现有的商机和订单记录设置默认用户ID"""
    app = create_app()
    
    with app.app_context():
        # 获取第一个管理员用户作为默认用户
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            print("未找到管理员用户，创建一个默认管理员用户")
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("已创建默认管理员用户: admin/admin123")
        
        # 为现有的商机记录设置默认用户ID
        opportunities = Opportunity.query.filter(Opportunity.user_id.is_(None)).all()
        print(f"找到 {len(opportunities)} 个商机需要设置用户ID")
        
        for opportunity in opportunities:
            opportunity.user_id = admin_user.id
            
        # 为现有的订单记录设置默认用户ID
        orders = Order.query.filter(Order.user_id.is_(None)).all()
        print(f"找到 {len(orders)} 个订单需要设置用户ID")
        
        for order in orders:
            order.user_id = admin_user.id
            
        # 提交更改
        db.session.commit()
        print(f"已为 {len(opportunities)} 个商机和 {len(orders)} 个订单设置默认用户ID")

if __name__ == '__main__':
    set_default_user_id()
    print("默认用户ID设置完成!")