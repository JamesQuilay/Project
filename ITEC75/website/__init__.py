from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from flask_login import LoginManager
#from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ITEC75_Project'
    
    

    # Use environment variables for sensitive information
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{getenv('DB_USERNAME')}:"  
        f"{getenv('DB_PASSWORD')}@" 
        f"{getenv('DB_HOST')}/"
        f"{getenv('DB_NAME')}"
    )


    db.init_app(app)
    

    from .views import views
    from .auth import auth
    

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')