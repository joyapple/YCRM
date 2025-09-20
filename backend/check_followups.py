from app import create_app
from models import db, FollowUp

app = create_app()
with app.app_context():
    followups = FollowUp.query.all()
    print('Total followups:', len(followups))
    for followup in followups:
        print(f'FollowUp ID: {followup.id}, User ID: {followup.user_id}, Customer ID: {followup.customer_id}')