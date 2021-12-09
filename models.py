from run import db

# Admin
class Profile(db.Model):
    profile_name=db.Column(db.String(100))
    profile_email = db.Column(db.String(100))
    profile_age = db.Column(db.String(100))
    profile_form = db.Column(db.String(100))
    about = db.Column(db.Text(1))

# Blog
class Blogs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    blog_name=db.Column(db.String(50))
    blog_url = db.Column(db.String(250))
    blog_dateTime = db.Column(db.String(70))
    blog_img = db.Column(db.String(150))
    date = db.Column(db.Date)   
