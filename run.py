from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate  
import os

app=Flask(__name__)
UPLOAD_FOLDER = 'static/assets/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db=SQLAlchemy(app)
migrate = Migrate(app, db)


# db.session.commit()
from models import *

#app routes
from app.routes import *

#admin routes
from admin.routes import *

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)    