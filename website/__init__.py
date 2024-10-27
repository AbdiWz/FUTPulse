from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
USER_DB_NAME = "users.db"
FUT_DB_NAME = 'fut.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ajkldjdifoi2'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{USER_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {
        'two': f'sqlite:///{FUT_DB_NAME}'
    }
    db.init_app(app)
    #Import Blueprints
    from .views import views
    from .auth  import auth
    #Import Models
    from .models import User
    #Create DBs
    with app.app_context():
        db.create_all()
    #Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    #Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #Load User Data from Users.db
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app