from enum import unique
from flask_login.mixins import UserMixin
from run import db

# Admin
class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    profile_name=db.Column(db.String(100))
    profile_email = db.Column(db.String(100))
    profile_age = db.Column(db.String(100))
    profile_address = db.Column(db.String(100))
    profile_phone = db.Column(db.String(50))
    about = db.Column(db.Text)

# Blog
class Blogs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    blog_name=db.Column(db.String(50))
    blog_url = db.Column(db.String(250))
    blog_dateTime = db.Column(db.String(70))
    blog_img = db.Column(db.String(150))
    date = db.Column(db.Date)   

# Skills
class Skills(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    skills_title=db.Column(db.String(100))
    skills_class = db.Column(db.String(50))

# Projects
class Projects(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    project_name = db.Column(db.String(100))
    project_img = db.Column(db.String(100))
    project_view_url = db.Column(db.Text)
    project_github_url = db.Column(db.Text)

# Feedback
class Feedbacks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    feedback_photo = db.Column(db.String(100))
    feedback_name = db.Column(db.String(100))
    feedback_from = db.Column(db.String(100))
    feedback_detail = db.Column(db.Text)

# Contact
class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_message = db.Column(db.Text)

# Login
class Login(UserMixin ,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    admin_username = db.Column(db.String(50))
    admin_password = db.Column(db.String(50))
    log_bool = db.Column(db.Boolean)

