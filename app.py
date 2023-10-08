from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///score.db")

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