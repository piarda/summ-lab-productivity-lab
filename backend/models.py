from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    bets = db.relationship('Bet', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class Bet(db.Model):
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    odds = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(20), nullable=False, default='Pending')    # Win, Lose, Pending
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    bet_type = db.Column(db.String(50), nullable=True)
    sport = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def payout(self):
        if self.result == 'Win':
            return round(self.amount * self.odds, 2)
        return 0.00

    def __repr__(self):
        return f'<Bet {self.event} - {self.result}>'
