from app import app
from models import db, User, Bet
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

with app.app_context():
    db.drop_all
    db.create_all

    user1 = User(username='piarda', password_hash=generate_password_hash('password123'))
    user2 = User(username='nywah', password_hash=generate_password_hash('password456'))

    db.session.add_all([user1, user2])
    db.session.commit()

    bet1 = Bet(
        event='Super Bowl 2025',
        amount=100,
        odds=2.5,
        result='Pending',
        date=datetime(2025, 2, 10, 20, 0, 0, tzinfo=timezone.utc),
        bet_type='Moneyline',
        sport='NFL',
        user_id=user1.id
    )

    bet2 = Bet(
        event='NBA Finals 2025',
        amount=50,
        odds=1.8,
        result='Pending',
        date=datetime(2025, 6, 15, 19, 0, 0, tzinfo=timezone.utc),
        bet_type='Spread',
        sport='NBA',
        user_id=user2.id
    )

    db.session.add_all([bet1, bet2])
    db.session.commit()

    print("Seeding complete")