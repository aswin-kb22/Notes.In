from flask import Flask,request,render_template,redirect,send_from_directory,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)
class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    filename=db.Column(db.String(200),nullable=False)
    subject=db.Column(db.String(200),nullable=False)
    branch=db.Column(db.String(200),nullable=False)
    semester=db.Column(db.Integer,nullable=False)
    upload_date=db.Column(db.DateTime,default=datetime.utcnow)
    #uploaded_by=db.Column(db.String(200),nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.user_id"),
        nullable=False
    )
    def __repr__(self):
        return f"<Note {self.id}>"

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    # joined_on = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship(
        "Note",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<User {self.user_id}>"


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    if user and user.password==password:
        session["user_id"]=user.user_id
        session["username"]=username
        return redirect('/home')
    else:
        return "Invalid username or password"
    

@app.route("/register_page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    if user is None:
        new=User(
            username=username,
            password=password
        )
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"An error occurred while registering the user: {str(e)}"
    else:
        return "username exists"
@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect('/')
    notes = Note.query.order_by(
        Note.upload_date.desc()
    ).all()

    return render_template(
        "index.html",
        notes=notes
    )

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form['title']
    subject= request.form['subject']
    branch = request.form['branch']
    semester=request.form['semester']

    file =request.files['note']

    filename=file.filename
    file.save(os.path.join('uploads',filename))

    user_id=session.get("user_id")
    new_note=Note(
        title=title,
        subject=subject,
        branch=branch,
        semester=semester,
        filename=filename,
        upload_date=datetime.utcnow(),
        user_id=session["user_id"]
    )
    if "user_id" not in session:
        return redirect("/")
    try:
        db.session.add(new_note)
        db.session.commit()
        return redirect('/home')
    except Exception as e:
        return f"An error occurred while uploading the note: {str(e)}"

@app.route("/download/<int:id>")
def download(id):
    note=Note.query.get_or_404(id)
    return send_from_directory(
        directory="uploads",
        path=note.filename,
        as_attachment=True
    )

@app.route("/preview/<int:id>")
def preview(id):
    note=Note.query.get_or_404(id)
    return send_from_directory(
        directory="uploads",
        path=note.filename,
        as_attachment=False
    )

@app.route("/search", methods=["GET"])
def search():
    search_txt=request.args.get("query")
    result = Note.query.filter(
        (Note.title.contains(search_txt)) |
        (Note.subject.contains(search_txt))
    ).all()
    return render_template("index.html", notes=result)

@app.route("/upload_page")
def upload_page():
    if "user_id" not in session:
        redirect("/")
    return render_template("upload.html")

@app.route("/mynotes",methods=["GET"])
def mynotes():
    if "user_id" not in session:
        return redirect('/')
    user_id=session['user_id']
    notes=Note.query.filter_by(user_id=user_id).order_by(Note.upload_date).all()
    return render_template("mynotes.html",notes=notes)

@app.route("/profile")
def profile():
    if "user_id" not in session:
        redirect("/")
    user=User.query.get_or_404(session["user_id"])
    notes_count=Note.query.filter_by(
        user_id=session["user_id"]
    ).count()
    return render_template("profile.html",user=user,notes_count=notes_count)

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect("/")
    user = User.query.get_or_404(session["user_id"])
    for note in user.notes:
        file_path = os.path.join("uploads", note.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(user)
    db.session.commit()
    session.clear()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    delete_note=Note.query.get_or_404(id)
    if delete_note.user_id != session["user_id"]:
        return "Unauthorized"
    try:
        db.session.delete(delete_note)
        db.session.commit()
        return redirect("/mynotes")
    except Exception as e:
        return f"An error occurred while deleting the note: {str(e)}"

@app.route("/edit_notes/<int:id>")
def edit_notes(id):
    edit_note=Note.query.get_or_404(id)
    if edit_note.user_id != session["user_id"]:
        return redirect("/")
    return render_template("edit.html",note=edit_note)
    
@app.route("/edit_details/<int:id>",methods=["POST","GET"])
def edit_details(id):
    edited_note=Note.query.get_or_404(id)
    if edited_note.user_id!=session["user_id"]:
        return redirect("/")
    edited_note.title=request.form['title']
    edited_note.subject=request.form['subject']
    edited_note.branch=request.form['branch']
    edited_note.semester=request.form['semester']
    db.session.commit()
    return redirect("/mynotes")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 