from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)).fetchone()
        if user:
            session["user"] = user[1]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        db.execute("INSERT INTO users VALUES (NULL, ?, ?)", (email, password))
        db.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    db = get_db()
    tickets = db.execute("SELECT * FROM tickets").fetchall()
    return render_template("dashboard.html", tickets=tickets)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        db = get_db()
        db.execute("INSERT INTO tickets VALUES (NULL, ?, ?, 'Open')", (title, desc))
        db.commit()
        return redirect("/dashboard")
    return render_template("create_ticket.html")

app.run(debug=True)
