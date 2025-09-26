from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, bcrypt
from resources.auth import auth_bp
from resources.bet import bet_bp

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Use os.environ.get in real apps

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(bet_bp, url_prefix="/bets")

if __name__ == '__main__':
    app.run(debug=True)
