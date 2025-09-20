from app import create_app
from models import db, Opportunity

app = create_app()
with app.app_context():
    opportunities = Opportunity.query.all()
    print('Total opportunities:', len(opportunities))
    for opportunity in opportunities:
        print(f'Opportunity ID: {opportunity.id}, User ID: {opportunity.user_id}, Name: {opportunity.name}')