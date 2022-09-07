# import modules
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error, lookup, lookup_specific
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

# create global list of types
types = ["title", "author", "isbn"]

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

        # create default shelves
        default_shelves = ["to read", "reading", "read"]
        id = db.execute("SELECT id FROM users WHERE username = ?", username)["id"]

        for shelf_name in default_shelves:
            db.execute("INSERT INTO shelves (user_id, name) VALUES (?, ?)", id, shelf_name)

        return redirect("/")

    else:
        return error("")

@app.route("/")
def home():
    # if user isn't logged in, redirect to login
    if session.get("user_id") == None:
        return redirect("/login")
    return render_template("index.html")

@app.route("/books")
def books():
    
    # ensure user is logged in 
    if session.get("user_id") == None:
        return redirect("/login")

    # get user info
    id = session["user_id"]
    shelves = db.execute("SELECT id, name FROM shelves WHERE user_id = ?", id) 

    # ensure GET is being used
    if request.method == "GET":
        if request.args.get("shelf_id") == None:
            return render_template("shelves.html", shelves=shelves, shelf=None)
        else:
            id = request.args.get("shelf_id")
            shelf = db.execute("SELECT name FROM shelves WHERE id = ?", id)
            return render_template("shelf.html", shelf="")
    
    else:
        return error("invalid request")

@app.route("/shelf")
def shelf():

    # ensure user is logged in
    if session.get("user_id") == None:
        return redirect("/login")

    shelf_id = request.args.get("shelf_id")
    id = session["user_id"]

    # get books from shelf
    books_isbns = db.execute("SELECT ISBN FROM books WHERE shelf_id = ?", shelf_id)

    # add book details to list
    books = []
    for isbn in books_isbns:
        book = lookup_specific(isbn["ISBN"], types)
        if book != None:
            books.append(book)

    return render_template("shelf.html", books=books) 



@app.route("/search", methods=["GET", "POST"])
def search():
    
    # intitle: Returns results where the text following this keyword is found in the title.
    # inauthor: Returns results where the text following this keyword is found in the author.
    # isbn: Returns results where the text following this keyword is the ISBN number.
    # inpublisher: Returns results where the text following this keyword is found in the publisher.


    # make sure user is logged in
    if session.get("user_id") == None:
        return redirect("/login")

    # if no search has been typed in, return default search page
    if request.method == "GET":    
        return render_template("search.html", types=types)

    # if something is submitted, search to API and return result
    elif request.method == "POST":
        search = request.form.get("search")
        type = request.form.get("type")
        
        # validate user input
        if search == None:
            return error("required fields not filled")
        if type not in types:
            return error("invalid type")

        # make API call
        response = lookup(search, type, types)
        
        if response == None:
            return render_template("search.html", response=None, types=types)
        else:
            return render_template("search.html", response=response, types=types)
    
    else:
        return error("")

@app.route("/details", methods=["GET"])
def details():
    # make sure user is logged in
    if session.get("user_id") == None:
        return redirect("/login")

    if request.method == "GET":
        isbn = request.args.get("isbn")

        # validate URL
        if isbn == None:
            return error("invalid key")

        # find correct book
        book = lookup_specific(isbn, types)
        
        return render_template("book_details.html", book=book)
    
    else:
        return error("error")

@app.route("/add", methods=["GET", "POST"])
def add():

    # make sure user is logged in
    if session.get("user_id") == None:
        return redirect("/login")

    # get user info
    id = session["user_id"]
    shelves = db.execute("SELECT * FROM shelves WHERE user_id = ?", id)

    # if page is loaded standardly:
    if request.method == "GET":
        isbn = request.args.get("isbn")

        # find book
        book = lookup_specific(isbn, types)

        return render_template("add.html", book=book, shelves=shelves)

    # if request to add is submitted:
    elif request.method == "POST":
        shelf_id = request.form.get("shelf")
        isbn = request.form.get("isbn")

        # insert into database
        db.execute("INSERT INTO books (shelf_id, ISBN) VALUES (?, ?)", shelf_id, isbn)

        return redirect("/")

    else:
        return error("")
