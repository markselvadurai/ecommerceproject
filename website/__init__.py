from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager 
from flask_login.login_manager import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
# storename = "https://mark-ecommerce-project.myshopify.com"
# def create_session():
#     # s = requests.Session()
#     # s.headers.update({
#     #     "X-SHOPIFY-Access-Token": "0709a06a3e0dac1d114bab4b2663df9a",
#     #     "Content-Type": "application/json"
#     # })
#     return s


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'banwbu hduiwh23128973awd121u78eyh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    
    # sess = create_session()
    # resp = sess.get(storename + "/api/2023-07/graphql.json")
    # print(resp.json())

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database!")