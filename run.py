from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    content=db.Column(db.Text)
    date=db.Column(db.Text)
    file=db.Column(db.Text)
    complete=db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("admin/blog.html", todos=todos)

@app.route("/add",methods=["GET","POST"])   
def add():
    title=request.form.get("title")
    content=request.form.get("content")
    date=request.form.get("date")
    file=request.form.get("file")
    newTodo=Todo(title=title,content=content,date=date,file=file,complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    edit = Todo.query.filter_by(id=id).first()
    if request.method == "POST":
        edit = Todo.query.filter_by(id=id).first()
        edit.title=request.form['title']
        edit.content=request.form['content']
        edit.date=request.form.get("date")
        edit.file=request.form.get("file")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("admin/update_base.html",edit=edit)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)