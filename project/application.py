import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///scrum.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        task_id=request.form.get("task_id")
        status=request.form.get("status")
        db.execute("UPDATE tasks SET status= :status WHERE task_id= :task_id", task_id=task_id, status=status)

        return redirect("/")

    else:
        rows3 = db.execute("SELECT * FROM tasks")
        rows2 = db.execute("SELECT * FROM tasks")
        rows = db.execute("SELECT * FROM tasks")
        return render_template("home.html", rows=rows, rows2=rows2, rows3=rows3)



@app.route("/collab", methods=["GET", "POST"])
@login_required
def collab():
    if request.method == "POST":
        employee=request.form.get("employee")
        db.execute("INSERT INTO collaborators (employee) VALUES(:employee)", employee=employee)
        return redirect("/collab")

    else:
        rowsc = db.execute("SELECT * FROM collaborators")
        return render_template("collab.html", rowsc=rowsc)


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        task_id=request.form.get("task_id")
        employee=request.form.get("employee")
        task=request.form.get("task")
        db.execute("INSERT INTO tasks (task_id,employee,task) VALUES(:task_id, :employee,:task)", task_id=task_id, employee=employee, task=task)
        return redirect("/tasks")
    else:
        rows = db.execute("SELECT * FROM tasks")
        rows2= db.execute("SELECT employee FROM collaborators")

        return render_template("tasks.html",rows=rows, rows2=rows2)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("not provide a username", "One does not simply")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", "One does not simply")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("provide an invalid username or password", "One does not simply")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # if any field is left blank, apology
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("submit an incomplete registration", "One does not simply")

        # if password does not equal confirm pass
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("submit an invalid password confirmation", "One does not simply")

        # hash password
        hash = generate_password_hash(request.form.get("password"))
        # insert username and password into users
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)

        #if username is not new
        if not new_user:
            return apology("use a taken username", "One does not simply")

        session["user_id"] = new_user
        return redirect("/")

    else:
        return render_template("register.html")






#error handling

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)