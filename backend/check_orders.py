from app import create_app
from models import db, Order

app = create_app()
with app.app_context():
    orders = Order.query.all()
    print('Total orders:', len(orders))
    for order in orders:
        print(f'Order ID: {order.id}, User ID: {order.user_id}, Amount: {order.amount}')