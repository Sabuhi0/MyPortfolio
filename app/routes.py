#app/routes

from flask import render_template,redirect,url_for,request
from admin.routes import blog,feedback,skills,project,contact
from run import app



@app.route("/")
def portfolio():
    from models import Blogs
    from models import Profile
    from models import Skills
    from models import Projects
    from models import Feedbacks
    from models import Contact
    prof= Profile.query.get(1)
    blogs = Blogs.query.all()
    skills = Skills.query.all()
    projects = Projects.query.all()
    feedbacks = Feedbacks.query.all()
    messages = Contact.query.all()
    return render_template("app/index.html",blogs=blogs,prof=prof,skills=skills,projects=projects,feedbacks=feedbacks,messages=messages)