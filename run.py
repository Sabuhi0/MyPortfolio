from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate  
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database. Railway/Heroku inject DATABASE_URL when a Postgres service is linked;
# without it we fall back to SQLite. SQLITE_PATH may point at a mounted volume so
# the file survives a redeploy - the container filesystem itself does not.
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Those providers still hand out the legacy scheme, SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # "sqlite:///" + "app.db" is relative, + "/data/app.db" becomes an absolute path
    DATABASE_URL = "sqlite:///" + os.getenv("SQLITE_PATH", "app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Uploads live on the container filesystem too, so this is also volume-friendly.
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/assets/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# Contact form notifications go to Telegram; leave the vars empty to turn them off.
app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN')
app.config['TELEGRAM_CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID')
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

# db.session.commit()
from models import *
migrate = Migrate(app, db)

# A fresh deploy starts with an empty database, so create anything that is missing.
# Existing tables are left untouched.
with app.app_context():
    db.create_all()

#app routes
from app.routes import *

#admin routes
from admin.routes import *

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)