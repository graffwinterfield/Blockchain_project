from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()

from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    from app_main.views import MyAdminIndexView, MyModelView
    admin = Admin(app, index_view=MyAdminIndexView(url='/IBB'), template_mode='bootstrap4')
    admin.add_view(MyModelView(User, db.session))

    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
