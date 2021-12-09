from run import db

# Admin
class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    profile_name=db.Column(db.String(100))
    profile_email = db.Column(db.String(100))
    profile_age = db.Column(db.String(100))
    profile_from = db.Column(db.String(100))
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
    skills_content = db.Column(db.Text) 
    skills_class = db.Column(db.String(50))

# Projects
class Projects(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    project_url = db.Column(db.Text)
    project_img = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    project_detail = db.Column(db.String(100))