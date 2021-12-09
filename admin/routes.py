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
    

