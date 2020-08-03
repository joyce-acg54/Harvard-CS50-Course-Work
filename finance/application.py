import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    portfolio = {}

    for stock in stocks:
        portfolio[stock["symbol"]] = lookup(stock["symbol"])

    balance = users[0]["cash"]
    total = balance

    return render_template("portfolio.html", portfolio=portfolio, stocks=stocks, total=total, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        buy = lookup(request.form.get("symbol"))

        if buy == None:
            return apology("Stock does not exist")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("You cannot purchase this number")

        # Select how much cash the user currently has
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        balance = rows[0]["cash"]
        price = buy["price"]

        cost = price * shares

        if cost > balance:
            return apology("You do not have enough funds to purchase this amount of shares!")

        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=cost, user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.form.get("username","")

    taken_usernames = db.execute("SELECT username FROM users")

    if not len(str(username)) > 0:
        return jsonify(False)
    for taken_username in taken_usernames:
        if username == taken_username["username"]:
            return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    purchased = db.execute("SELECT symbol, shares, price, order_id FROM purchases WHERE user_id = :user_id ORDER BY order_id ASC", user_id=session["user_id"])

    return render_template("history.html", purchased=purchased)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = usd(lookup(request.form.get("symbol")))

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # if any field is left blank, apology
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Sorry, you must complete all fields to register!")

        # if password does not equal confirm pass
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Sorry, your confirmation doesn't match the password you typed in")

        # hash password
        hash = generate_password_hash(request.form.get("password"))
        # insert username and password into users
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)

        #if username is not new
        if not new_user:
            return apology("username taken")

        session["user_id"] = new_user
        return redirect("/")

    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        sell = lookup(request.form.get("symbol"))

        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("You cannot sell less than or 0 shares")

        # check shares
        stock = db.execute("SELECT SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol", user_id=session["user_id"], symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("You cannot sell less than 0 or more than the stocks you have!")

        # checks user name
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # balance in account
        balance = rows[0]["cash"]
        price = sell["price"]

        # Calculate the price of requested shares
        total_price = price * shares

        # Book keeping (TODO: should be wrapped with a transaction)
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=price)


        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

        return render_template("sell.html", stocks=stocks)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)