from app import create_app
from models import db, Customer

app = create_app()
with app.app_context():
    customers = Customer.query.all()
    print('Total customers:', len(customers))
    for customer in customers:
        print(f'Customer ID: {customer.id}, Assigned To: {customer.assigned_to}, Name: {customer.name}')