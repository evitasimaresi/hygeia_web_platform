from flask import Flask, session
from flask_session import Session
from config import Config
from app.models import db
from app.commands import import_specialties, reimport_db
import os


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configure session
app.config["SESSION_PERMANENT"] = Config.SESSION_PERMANENT
app.config["SESSION_TYPE"] = Config.SESSION_TYPE
Session(app)


from app.models import User

# Create the database file
# Delete the "initialized.flag" when I want to reinitialize the DB
def initialize_database():
    with app.app_context():
        db.create_all()
        import_specialties()
        reimport_db()
        open('initialized', 'w').close()

if not os.path.exists('initialized'):
    initialize_database()
else:
    print("DB already initialized.")


from app import routes
