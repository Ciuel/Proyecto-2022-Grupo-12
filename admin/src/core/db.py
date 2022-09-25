from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
#from flask_migrate import Migrate

database = SQLAlchemy()
from src.core.auth.user import User
from src.core.board.discipline import Discipline
from src.core.board.associate import Associate
from src.core.auth.role import Role
from src.core.board.payment import Payment
from src.core.auth.permission import Permission
#migrate = Migrate()

def init_app(app):
    database.init_app(app)
    config_db(app)
    #migrate.init_app(app, db)

def config_db(app):
    @app.before_first_request
    def create_tables():
        database.create_all()
    
    @app.teardown_appcontext
    def close_session(exception=None):
        database.session.remove()

def reset_db():
    print("   Deleting database...")
    database.drop_all()
    print("   Creating database ...")
    database.create_all()
    print("   All done!")
