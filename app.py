# import modules
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error
import cs50

# initiate flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# make sure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ensure responses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# initiate sql database
db = cs50.SQL("sqlite:///bookworm.db")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"username: {username} password: {password}")

        username_db = db.execute("SELECT * FROM users WHERE username = ?", username)

        #validate user input
        if username == None or password == None:
            return error("required fields not filled")
        if username_db == []:
            return error("username not found")
        
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/")
    else:
        return error("")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["user_id"] = None
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # validate user input
        if username == None or password == None or password_confirm == None:
            return error("required fields not filled")
        if password != password_confirm:
            return error("passwords don't match")

        # ensure username is unique
        existing_usernames = []
        for user in db.execute("SELECT username FROM users"):
            existing_usernames.append(user["username"])

        if username in existing_usernames:
            return error("username taken")

        # add to database
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/")

    else:
        return error("")

@app.route("/")
def home():
    if session.get("user_id") == None:
        return redirect("/login")
    return render_template("index.html")