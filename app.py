from flask import Flask, render_template, request, redirect, flash, session
from cs50 import SQL
import os
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///score.db")
udb = SQL("sqlite:///user.db")
app.config.update(SECRET_KEY=os.urandom(24))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST": 
        name = request.form.get("name")
        score = request.form.get("score")

        db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name, score)

        return redirect("/")

    else:

        students = db.execute("SELECT * FROM score")
        return render_template("index.html", students=students)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        score = db.execute("SELECT * FROM score WHERE id = ?", id)[0]
        print(score)
        return render_template("edit.html", score=score)
    elif request.method == "POST":
        score_name = request.form.get("name")
        score_score = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_score, id)
        return redirect("/")
    
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/")

@app.route("/register", methods=['POST', 'GET'])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        rows = udb.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

        email = request.form.get("email")
        name_user = request.form.get("name_user")
        username = request.form.get("username")
        password = request.form.get("password")
        rpassword = request.form.get("rpassword")

        hash = generate_password_hash(password)
        if len(rows) == 1:
            return "username already taken"
        if password == rpassword:
            udb.execute("INSERT INTO user (username, password) VALUES(?, ?)", username, hash)

            registered_user = udb.execute("select * from user where username = ?", username)
            session["id"] = registered_user[0]["id"]
            flash("you were sucessfully registered")
            return redirect("/")

        else:

            return render_template("register.html", userdb=userdb)
        
    else:
        return render_template("register.html")