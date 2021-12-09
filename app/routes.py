#app/routes

from flask import render_template,redirect,request
from admin.routes import blog,skills
from run import app



@app.route("/")
def portfolio():
    from models import Blogs
    from models import Profile
    from models import Skills
    prof= Profile.query.get(1)
    blogs = Blogs.query.all()
    skills = Skills.query.all()
    return render_template("app/index.html",blogs=blogs,prof=prof,skills=skills)