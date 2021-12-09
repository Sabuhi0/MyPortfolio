#app/routes

from flask import render_template,redirect,request
from admin.routes import blog
from run import app



@app.route("/")
def portfolio():
    from models import Blogs
    from models import Profile
    prof= Profile.query.get(1)
    blogs = Blogs.query.all()
    return render_template("app/index.html",blogs=blogs,prof=prof)