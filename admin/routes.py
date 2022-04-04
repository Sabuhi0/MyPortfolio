# admin/routes

import flask
from flask_login.utils import login_user
from flask_mail import Message
from run import app 
from flask import Flask,render_template,url_for,redirect,request
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from run import login_manager

# Login
@login_manager.user_loader
def load_user(user_id):
    from models import Login
    return Login.query.get(int(user_id))

@app.route("/login",methods=["GET","POST"])
def admin_login():
    from models import Login
    from run import db
    login = Login(
        admin_username = "admin",
        admin_password = "admin",
        log_bool = False
    )
    db.session.add(login)
    db.session.commit()
    
    if request.method == "POST":
        if login.admin_username == request.form["admin_username"] and login.admin_password == request.form["admin_password"]:
            login_user(login, remember=login.log_bool)
            return redirect (url_for("profile"))

        else:
            return redirect(url_for("admin_login"))

    return render_template("admin/login.html", login = login)

# Logout
@app.route("/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect (url_for("portfolio"))

# Admin Profile
@app.route("/admin",methods=["GET","POST"])
@login_required
def profile():
    from models import Profile
    from run import db

    prof = Profile(
        profile_name = "Sabuhi Gasimov",
        profile_email = "sabuhiq0gmail.com",
        profile_age = "17",
        profile_address = "Baku, Azerbaijan",
        profile_phone = "+994 55 234 62 50",
        about = "I started this field at the age of 17, which I have been interested in since childhood. I am studying web development through Pragmatech Education. I have knowledge of HTML, CSS, BootStrap, Animated CSS, JavaScript, Git & GitHub, Sass, Less, Tailwind Css, Python, SQL, Flask. I create creative and high-level sites."
    )
    db.session.add(prof)
    db.session.commit()
    if request.method == "POST":
        prof=Profile.query.get(1)

        prof.profile_name=request.form['prof_name']
        prof.profile_email=request.form['prof_email']
        prof.profile_age=request.form['prof_age']
        prof.profile_address=request.form['profile_address']
        prof.profile_phone=request.form['profile_phone']
        prof.about=request.form['prof_about']
        db.session.commit()
        return redirect("/")
    return render_template("admin/profile.html",prof = Profile.query.get(1))


# Admin Blog
@app.route("/admin/blog",methods=["GET","POST"])
@login_required
def blog():
    from models import Blogs
    import os
    from run import db
    from werkzeug.utils import secure_filename
    from datetime import date
    blogs = Blogs.query.all()
    if request.method=="POST":
        current = date.today()
        file = request.files['blog_img']
        filename = secure_filename(file.filename)   
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog_name = request.form["blog_name"]
        blog_url = request.form["blog_url"]
        blog_dateTime = request.form["blog_dateTime"]
        blog = Blogs(
            blog_name = blog_name,
            blog_url = blog_url,
            blog_dateTime = blog_dateTime,
            blog_img = os.path.join(app.config['UPLOAD_FOLDER'], filename),
            date=current
        )
        db.session.add(blog)
        db.session.commit()
        return redirect("/")
    return render_template("admin/blog.html", blogs=blogs)

@app.route("/blogDelete/<int:id>",methods=["GET","POST"])
@login_required
def blog_delete(id):
    from models import Blogs
    import os
    from run import db
    blogs = Blogs.query.filter_by(id=id).first()
    filename = blogs.blog_img
    os.unlink(os.path.join(filename))
    db.session.delete(blogs)
    db.session.commit()
    return redirect ("/admin/blog")

@app.route("/blogEdit/<int:id>",methods=["GET","POST"])
@login_required
def blog_edit(id):
    from models import Blogs
    from run import db
    newBlogs = Blogs.query.filter_by(id=id).first()
    if request.method=="POST":
        blogs = Blogs.query.filter_by(id=id).first()
        blogs.blog_name = request.form["blog_name"]
        blogs.blog_url = request.form["blog_url"]
        blogs.blog_dateTime = request.form["blog_dateTime"]
        db.session.commit()
        return redirect("/")
    return render_template ("/admin/update_blog.html",newBlogs=newBlogs)
    

# Admin Skills
@app.route("/admin/skills",methods=["GET","POST"])
@login_required
def skills():
    from models import Skills
    from run import db
    skills = Skills.query.all()
    if request.method=="POST":
        skills_title = request.form["skills_title"]
        skills_content = request.form["skills_content"]
        skills_class = request.form["skills_class"]
        skill = Skills(
            skills_title = skills_title,
            skills_content = skills_content,
            skills_class = skills_class
        )
        db.session.add(skill)
        db.session.commit()
        return redirect("/")
    return render_template("admin/skills.html", skills=skills)

@app.route("/skillDelete/<int:id>", methods=["GET","POST"])
@login_required
def skill_delete(id):
    from models import Skills
    from run import db
    skills = Skills.query.filter_by(id=id).first()
    db.session.delete(skills)
    db.session.commit()
    return redirect ("/admin/skills")

@app.route("/skillEdit/<int:id>",methods=["GET","POST"])
@login_required
def skill_edit(id):
    from models import Skills
    from run import db
    newSkill = Skills.query.filter_by(id=id).first()
    if request.method=="POST":
        skl = Skills.query.filter_by(id=id).first()
        skl.skills_title = request.form["skills_title"]
        skl.skills_content = request.form["skills_content"]
        skl.skills_class = request.form["skills_class"]
        db.session.commit()
        return redirect("/")
    return render_template ("/admin/update_skill.html",newSkill=newSkill)

# Admin Project
@app.route("/admin/projects",methods=["GET","POST"])
@login_required
def project():
    from models import Projects
    import os
    from run import db
    from werkzeug.utils import secure_filename
    projects = Projects.query.all()
    if request.method=="POST":
        file = request.files['project_img']
        filename = secure_filename(file.filename)   
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        project_name = request.form["project_name"]
        project_view_url = request.form["project_view_url"]
        project_github_url = request.form["project_github_url"]
        prjct = Projects(
            project_name = project_name,
            project_view_url = project_view_url,
            project_github_url = project_github_url,
            project_img = os.path.join(app.config['UPLOAD_FOLDER'], filename),
        )
        db.session.add(prjct)
        db.session.commit()
        return redirect("/")
    return render_template("admin/project.html", projects=projects)

@app.route("/projectDelete/<int:id>",methods=["GET","POST"])
@login_required
def project_delete(id):
    from models import Projects
    import os
    from run import db
    projects = Projects.query.filter_by(id=id).first()
    filename = projects.project_img
    os.unlink(os.path.join(filename))
    db.session.delete(projects)
    db.session.commit()
    return redirect ("/admin/projects")

@app.route("/projectEdit/<int:id>",methods=["GET","POST"])
@login_required
def project_edit(id):
    from models import Projects
    from run import db
    newProject = Projects.query.filter_by(id=id).first()
    if request.method=="POST":
        projects = Projects.query.filter_by(id=id).first()
        projects.project_name = request.form["project_name"]
        projects.project_view_url = request.form["project_view_url"]
        projects.project_github_url = request.form["project_github_url"]
        db.session.commit()
        return redirect("/")
    return render_template ("/admin/update_project.html",newProject=newProject)

# Admin Feedback
@app.route("/admin/feedback", methods=["GET","POST"])
@login_required
def feedback():
    from models import Feedbacks
    import os
    from run import db
    from werkzeug.utils import secure_filename
    feedbacks = Feedbacks.query.all()
    if request.method=="POST":
        file = request.files['feedback_imgProfil']
        filename = secure_filename(file.filename)   
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        feedback_name = request.form["feedback_name"]
        feedback_from = request.form["feedback_from"]
        feedback_detail = request.form["feedback_detail"]
        feedback = Feedbacks(
            feedback_name = feedback_name,
            feedback_from = feedback_from,
            feedback_detail = feedback_detail,
            feedback_photo = os.path.join(app.config['UPLOAD_FOLDER'], filename),
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect("/")
    return render_template("/admin/feedbacks.html",feedbacks=feedbacks)

@app.route("/feedbackDelete/<int:id>",methods=["GET","POST"])
@login_required
def feedback_delete(id):
    from models import Feedbacks
    import os
    from run import db
    feedbacks = Feedbacks.query.filter_by(id=id).first()
    filename = feedbacks.feedback_photo
    os.unlink(os.path.join(filename))
    db.session.delete(feedbacks)
    db.session.commit()
    return redirect ("/admin/feedback")

@app.route("/feedbackEdit/<int:id>",methods=["GET","POST"])
@login_required
def feedback_edit(id):
    from models import Feedbacks
    from run import db
    newFeedback = Feedbacks.query.filter_by(id=id).first()
    if request.method=="POST":
        feedbacks = Feedbacks.query.filter_by(id=id).first()
        feedbacks.feedback_name = request.form["feedback_name"]
        feedbacks.feedback_from = request.form["feedback_from"]
        feedbacks.feedback_detail = request.form["feedback_detail"]
        db.session.commit()
        return redirect("/")
    return render_template ("/admin/update_feedbacks.html",newFeedback=newFeedback)

# Admin Contact
@app.route("/admin/contact", methods=["GET","POST"])
@login_required
def contact():
    from models import Contact
    from run import db
    # import smtplib    
    from flask_mail import Mail,Message
    from run import mail
    messages = Contact.query.all()
    if request.method == "POST":
        contact_name = request.form["contact_name"]
        contact_email = request.form["contact_email"]
        contact_message = request.form["contact_message"]
        contact = Contact(
            contact_name = contact_name,
            contact_email = contact_email,
            contact_message = contact_message,
        )    
        myGmail = "sabuhiq0@gmail.com"
        msg = Message(contact_message,sender = contact_email, recipients = [myGmail])
        mail.send(msg)
        db.session.add(contact)
        db.session.commit()
        return redirect ("/")
    return render_template("/admin/contact.html", messages=messages)

@app.route("/contactDelete/<int:id>")
@login_required
def contact_delete(id):
    from models import Contact
    from run import db
    messages = Contact.query.filter_by(id=id).first()
    db.session.delete(messages)
    db.session.commit()
    return redirect ("/admin/contact")