# admin/routes

from run import app 
from flask import Flask,render_template,url_for,redirect,request

# Admin Profile

@app.route("/admin",methods=["GET","POST"])
def profile():
    from models import Profile
    from run import db

    prof = Profile(
        profile_name = "Sabuhi Gasimov",
        profile_email = "sabuhiq0gmail.com",
        profile_age = "19",
        profile_from = "Baku,Azerbaijan",
        about = "I help you build brand for your business at an affordable price. Thousands of clients have procured exceptional results while working with our dedicated team. when an unknown printer took a galley of type and scrambled it to make a type specimen book. Delivering work within time and budget which meets client’s requirements is our moto. Lorem Ipsum has been the industry's standard dummy text ever when an unknown printer took a galley. Lorem Ipsum has been the industry's standard dummy text ever when an unknown printer took a galley."
    )
    db.session.add(prof)
    db.session.commit()
    if request.method == "POST":

        prof=Profile.query.get(1)

        prof.profile_name=request.form['prof_name']
        prof.profile_email=request.form['prof_email']
        prof.profile_age=request.form['prof_age']
        prof.profile_from=request.form['prof_from']
        prof.about=request.form['prof_about']
        db.session.commit()
        return redirect("/")
    return render_template("admin/profile.html",prof = Profile.query.get(1))


# Admin Blog

@app.route("/admin/blog",methods=["GET","POST"])
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
    return render_template ("/admin/update_block.html",newBlogs=newBlogs)
    

# Admin Skills
@app.route("/admin/skills",methods=["GET","POST"])
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
        return redirect("/admin/skills")
    return render_template("admin/skills.html", skills=skills)

@app.route("/skillDelete/<int:id>", methods=["GET","POST"])
def skill_delete(id):
    from models import Skills
    from run import db
    skills = Skills.query.filter_by(id=id).first()
    db.session.delete(skills)
    db.session.commit()
    return redirect ("/admin/skills")

@app.route("/skillEdit/<int:id>",methods=["GET","POST"])
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
        project_detail = request.form["project_detail"]
        project_url = request.form["project_url"]
        prjct = Projects(
            project_name = project_name,
            project_detail = project_detail,
            project_url = project_url,
            project_img = os.path.join(app.config['UPLOAD_FOLDER'], filename),
        )
        db.session.add(prjct)
        db.session.commit()
        return redirect("/")
    return render_template("admin/project.html", projects=projects)

@app.route("/projectDelete/<int:id>",methods=["GET","POST"])
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
def project_edit(id):
    from models import Projects
    from run import db
    newProject = Projects.query.filter_by(id=id).first()
    if request.method=="POST":
        projects = Projects.query.filter_by(id=id).first()
        projects.project_name = request.form["project_name"]
        projects.project_detail = request.form["project_detail"]
        projects.project_url = request.form["project_url"]
        db.session.commit()
        return redirect("/")
    return render_template ("/admin/update_project.html",newProject=newProject)

# Admin Feedback
@app.route("/admin/feedback", methods=["GET","POST"])
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