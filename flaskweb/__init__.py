from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

migrate = Migrate()

app = Flask(__name__)
app.config['SECRET_KEY'] = '68a517e10f3ab14c1258d42a46b60004'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://track:track@localhost:5432/track"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

db.init_app(app)
migrate.init_app(app, db)

from flaskweb import routes