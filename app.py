# import modules
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from helpers import error, check_login

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
engine = create_engine("sqlite:///bookworm.db")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        return render_template("index.html")
    else:
        return render_template("error.html", link=error(""))

@app.route("/register", methods=["GET", "POST"])
def register():
    print(error(""))
    return render_template("error.html", link=error(""))

@app.route("/")
def home():
    if session.get("user_id") == None:
        return redirect("/login")
    return render_template("error.html")